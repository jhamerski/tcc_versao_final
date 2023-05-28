import scrapy
from pymongo import MongoClient
from scrapy.http import Request
from core.config import settings

class MeuSpider(scrapy.Spider):
    name = 'meu_spider'

    def start_requests(self):
        try:
            # Conecte-se ao MongoDB
            username = settings.MONGODB_USERNAME
            password = settings.MONGODB_PASSWORD
            host = settings.MONGODB_HOST

            client = MongoClient(username=username, password=password, host=host)
            db = client[f'{settings.MONGODB_DB}']
            collection = db['url']

            # Recupere as URLs do MongoDB
            resultados = collection.find()

            for item in resultados:
                url = item['link']
                yield scrapy.Request(url=url, callback=self.parse, meta={'url': url})

        except Exception as e:
            self.logger.error(f'Erro ao conectar-se ao MongoDB: {str(e)}')

        finally:
            client.close()

    def parse(self, response):
        url = response.meta['url']
        valor_atual = response.css('meta[property="og:title"]::attr(content)').get()  # Seletor para extrair o valor do atributo content da meta tag

        # Recupera o valor atual do banco
        username = settings.MONGODB_USERNAME
        password = settings.MONGODB_PASSWORD
        host = settings.MONGODB_HOST

        client = MongoClient(username=username, password=password, host=host)
        db = client[f'{settings.MONGODB_DB}']
        collection = db['url']

        resultado_banco = collection.find_one({'link': url})
        valor_no_banco = resultado_banco['valor_atual']

        if valor_atual == valor_no_banco:
            self.logger.info(f'O valor é igual para a URL: {url}')
        else:
            self.logger.info(f'O valor é diferente para a URL: {url}')

            # Atualiza o valor no banco
            collection.update_one({'link': url}, {'$set': {'valor_atual': valor_atual}})

            # Faça algo adicional se o valor for diferente, como criar uma solicitação HTTP usando o Scrapy
            payload = {'url': url, 'valor_anterior': valor_no_banco, 'valor_atual': valor_atual}
            request = Request(url='http://url_log', method='POST', body=payload)
            self.crawler.engine.schedule(request, self)
