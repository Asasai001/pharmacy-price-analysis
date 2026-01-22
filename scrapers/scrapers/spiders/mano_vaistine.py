import scrapy


class ManoVaistineSpider(scrapy.Spider):
    name = "mano_vaistine"
    allowed_domains = ["www.manovaistine.lt"]
    start_urls = ["https://www.manovaistine.lt/akcijos?_gl=1"]

    def parse(self, response):
        pass


product = response.css('div.product')
title = product.css('div.product-title h1::text').get()
company_name = product.css('div a.product-brand-link::text').get()
product_code = product.css('dl.product-attributes span.product-attribute-value::text').get()
old_price = product.css('span.product-price::text').get()
base_price = product.css('div.