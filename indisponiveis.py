from urllib.parse import quote_plus
from pymongo import MongoClient
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from time import sleep
import re
from core.config import settings

# Formata as credenciais para serem adicionadas no URI
formatted_username = quote_plus(settings.MONGODB_USERNAME)
formatted_password = quote_plus(settings.MONGODB_PASSWORD)
formatted_host = quote_plus(settings.MONGODB_LOCALHOST)

# Define o URI de conexão com autenticação
uri = f"mongodb://{formatted_username}:{formatted_password}@{formatted_host}/{settings.MONGODB_DB}"

client = MongoClient(uri)

# Acessa o banco de dados
db = client.get_database(f'{settings.MONGODB_DB}')
urls_collection = db.url
url_log_collection = db.url_log

browser = None


def start_browser(hide):
    global browser

    options = FirefoxOptions()
    if hide:
        options.add_argument('-headless')
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--no-sandbox")

    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0"
    options.add_argument(f"--user-agent={user_agent}")

    browser = webdriver.Firefox(options=options)
    browser.get("https://www.mercadolivre.com.br")
    WebDriverWait(browser, 10).until(lambda driver: driver.execute_script('return document.readyState') == 'complete')


def get_price_title_mercado_livre(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    meta_element = soup.find('meta', property='og:title')

    if meta_element and 'content' in meta_element.attrs:
        content = meta_element['content']
        price_match = re.search(r'R\$\s*([\d.,]+)', content)
        title_match = re.search(r'^(.*?) - R\$\s*', content)

        price = clean_price(price_match.group(1)) if price_match else None
        title = title_match.group(1) if title_match else None
        
        return title, price
    
    return None, None
    

def add_decimal_zeros(price):
    if len(price.split(".")[-1]) == 1:
        return price + "0"
    return price


def clean_price(price):
    price = price.replace("R$", "").replace(".", "").replace(",", "").strip()
    price = add_decimal_zeros(price)

    return price


def update_price(url, price, titulo):
    current_data = urls_collection.find_one({"link": url})

    # Atualiza a data da última consulta em urls_collection
    now = datetime.now() + timedelta(hours=-3)
    urls_collection.update_one({"link": url}, {"$set": {"ultima_consulta_em": now}})

    # Incrementa o contador qtd_consultas
    qtd_consultas = current_data.get("qtd_consultas", 0) + 1
    urls_collection.update_one({"link": url}, {"$set": {"qtd_consultas": qtd_consultas}})

    if current_data.get("titulo") == None:
        # Atualiza o título na coleção urls_collection
        urls_collection.update_one({"link": url}, {"$set": {"titulo": titulo}})

    # print(current_data.get("titulo"))

    # Verifica se o preço é diferente do valor atual
    if current_data and current_data.get("valor_atual") != price:
        # Atualiza o preço na coleção urls_collection
        urls_collection.update_one({"link": url}, {"$set": {"valor_atual": price}})

        # Insere o registro na coleção url_log com a data atual
        url_log = {"url": url, "valor_atual": price, "data_registro": now}
        url_log_collection.insert_one(url_log)
    elif current_data is None:
        # Caso seja a primeira consulta, preenche o valor na coleção urls_collection
        urls_collection.update_one({"link": url}, {"$set": {"valor_atual": price}})
    elif price is None:
        # Caso o valor do preço não seja encontrado, preenche o campo "error" com a mensagem padrão
        error_message = f"Erro ao tentar obter o valor do produto em {datetime.now() + timedelta(hours=-3)}"
        error_monitoramento = current_data.get("error_monitoramento", 0) + 1
        urls_collection.update_one({"link": url}, {"$set": {"error": error_message, "error_monitoramento": error_monitoramento}})
    elif price is not None:
        # Atualiza o campo "error_monitoramento" para zero
        urls_collection.update_one({"link": url}, {"$set": {"error_monitoramento": 0, "error": None}})
    else:
        # O preço é igual ao valor atual, não é necessário fazer nenhuma atualização
        pass 


def indisponiveis():
    filtro = {
        'error_monitoramento': {'$gt': 1}
    }

    # Construindo o pipeline da agregação
    pipeline = [
        {'$match': filtro},
        {'$sort': {'ultima_consulta_em': 1}},
        {'$limit': 1}
    ]

    # Executando a agregação
    resultado = db.url.aggregate(pipeline)

    # Obtendo o resultado
    for document in resultado:
        url = document.get('link')

        if "mercadolivre.com" in url:
            sleep(2)
            titulo, price = get_price_title_mercado_livre(url)
        else:
            # Caso o link não seja do Mercado Livre nem da Amazon, define o preço como None
            price = None
            titulo = None
        try:
            # Atualiza o preço na coleção urls_collection e insere o registro na coleção url_log
            update_price(url, price, titulo)
        except Exception as e:
            print(f'Erro ao obter o preço: {e}')


def close_connection():
    global client
    global browser

    if client:
        client.close()

    if browser:
        browser.quit()


def main():
    try:
        start_browser(True)
        indisponiveis()
    finally:
        close_connection()


if __name__ == '__main__':
    main()
