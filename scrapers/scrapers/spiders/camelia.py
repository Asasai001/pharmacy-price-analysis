import scrapy


class CameliaSpider(scrapy.Spider):
    name = "camelia"
    allowed_domains = ["camelia.lt"]
    start_urls = ["https://camelia.lt/akcijos"]

    def parse(self, response):
        products = response.css('div[data-test^="product-list-item"]')

        for product in products:
            yield {
                'name': product.css('div.product-name::text').get(),
                'price': product.css('div.price::text').get(),
            }




