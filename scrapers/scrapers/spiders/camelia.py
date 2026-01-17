import scrapy


class CameliaSpider(scrapy.Spider):
    name = "camelia"
    allowed_domains = ["camelia.lt"]
    start_urls = ["https://camelia.lt/akcijos"]

    def parse(self, response):
        goods = response.css("div.product-list")
        for good in goods:
            yield {
                'name': good.css('div.product-name::text').get(),
                'price': good.css('div.price::text').get(),
            }




