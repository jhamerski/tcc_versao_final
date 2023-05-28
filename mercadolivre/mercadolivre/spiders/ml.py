import scrapy


# class MlSpider(scrapy.Spider):
#     name = "ml"
#     start_urls = ["https://www.mercadolivre.com.br/ofertas"]

#     def parse(self, response):
#         # for i in range(4):
#         #     final = ['min', 'default', 'avg', 'sup']

#         for j in response.xpath(f'//li[@class="promotion-item avg"]'):
#             # price = j.xpath('.//span[@class="andes-money-amount__fraction"]//text()').getall()
#             # title = j.xpath('.//p[@class="promotion-item__title"]/text()').get()
#             # link = j.xpath('.//p[@class="promotion-item__link-container"]/text()').get()
#             # link = j.xpath('./a/@href')
#             link = response.css('a.promotion-item__link-container::attr(href)').get()
#             print(link)

#             yield {
#                 # 'price': price,
#                 # 'title': title,
#                 'link': link
#             }
#             next_page = response.xpath('//a[contains(@title, "Próxima")]/@href').get()
#             if next_page:
#                 yield scrapy.Request(url=next_page, callback=self.parse)
import scrapy

class MlSpider(scrapy.Spider):
    name = "ml"
    start_urls = ["https://www.mercadolivre.com.br/ofertas"]

    def __init__(self):
        super(MlSpider, self).__init__()
        self.visited_links = set()

    def parse(self, response):
        final = ['min', 'default', 'avg', 'sup']
        for j, value in enumerate(final):
            for item in response.xpath(f'//li[contains(@class, "promotion-item {value}")]'):
                link = item.css('a.promotion-item__link-container::attr(href)').get()

                if link not in self.visited_links:
                    self.visited_links.add(link)
                    yield {
                        'link': link
                    }

        next_page = response.xpath('//a[contains(@title, "Próxima")]/@href').get()
        if next_page:
            yield scrapy.Request(url=next_page, callback=self.parse)
