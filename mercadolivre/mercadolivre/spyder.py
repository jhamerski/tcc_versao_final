import scrapy
from pymongo import MongoClient
from urllib.parse import quote_plus
import requests
from pymongo import UpdateOne
from core.config import settings

class MeuSpider(scrapy.Spider):
    name = 'meu_spider'

    def start_requests(self):
        try:
            # Conecte-se ao MongoDB
            username = settings.MONGODB_USERNAME
            password = settings.MONGODB_PASSWORD
            host = settings.MONGODB_HOST

            # Formata as credenciais para serem adicionadas no URI
            formatted_username = quote_plus(username)
            formatted_password = quote_plus(password)
            formatted_host = quote_plus(host)

            # Define o URI de conexão com autenticação
            uri = f"mongodb://{formatted_username}:{formatted_password}@{formatted_host}/{settings.MONGODB_DB}"

            client = MongoClient(uri)
            db = client.get_database(f'{settings.MONGODB_DB}')
            collection = db['url']

            # Recupere as URLs do MongoDB
            resultados = collection.find()

            for item in resultados:
                url = item['url']
                link = item.css('a.promotion-item__link-container::attr(href)').get()

                if link:
                    yield scrapy.Request(url=link, callback=self.parse, meta={'url': url, 'collection': collection})

        except Exception as e:
            self.logger.error(f'Erro ao conectar-se ao MongoDB: {str(e)}')

        finally:
            client.close()

    def parse(self, response):
        url = response.meta['url']
        valor_xpath = None

        try:
            valor_xpath = response.xpath('sua_xpath').get()  # Substitua 'sua_xpath' pela sua expressão XPath para recuperar o valor desejado

            collection = response.meta['collection']

            resultado_banco = collection.find_one({'url': url})
            valor_no_banco = resultado_banco['valor']

            if valor_xpath and valor_xpath != valor_no_banco:
                update_operation = UpdateOne(
                    {'url': url},
                    {'$set': {'valor': valor_xpath}}
                )
                collection.bulk_write([update_operation])

                # Faça algo aqui se os valores forem diferentes
                # Por exemplo, envie o histórico para a URL de log
                payload = {'url': url, 'valor_anterior': valor_no_banco, 'valor_atual': valor_xpath}
                response = requests.post('http://url_log', data=payload)
                # Faça algo com a resposta, se necessário

        except Exception as e:
            self.logger.error(f'Erro ao processar a página {url}: {str(e)}')

        except KeyError:
            self.logger.error(f'Chave "valor" não encontrada no documento do MongoDB para a URL {url}')
