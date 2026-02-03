import scrapy
from scrapers.items import ProductItem

class GintarineSpider(scrapy.Spider):
    name = "gintarine"
    allowed_domains = ["www.gintarine.lt"]
    start_urls = ["https://www.gintarine.lt/akcijos-4"]

    custom_settings = {
        'FEEDS': {
            'gintarine_data.json': {
                'format': 'json',
                'overwrite': True,
                'encoding': 'utf-8'
            }
        }
    }

    def parse(self, response):
        products = response.css('div.product-item')
        for product in products:
            relative_url = product.css('a::attr(href)').get()
            full_url = response.urljoin(relative_url)
            yield scrapy.Request(url=full_url, callback=self.parse_product_page)


        current_page = response.meta.get("page", 1)
        next_page = current_page + 1

        if next_page <= 263:
            next_url = f"https://www.gintarine.lt/akcijos-4?pagenumber={next_page}"
            yield response.follow(
                next_url,
                callback=self.parse,
                meta={"page": next_page},
            )

    def parse_product_page(self, response):
        product = response.css('main.single-product')
        gintarine_discount_percentage = product.css('div.ribbon::text').get()

        product_item = ProductItem()

        product_item["url"] = response.url
        product_item["title"] = product.css('h1.single-product__title::text').get()
        product_item["company_name"] = product.css('div.single-product__brand a::text').get()
        product_item["category"] = response.css('ul.breadcrumbs a.breadcrumbs__link span::text').getall()[1]
        product_item["sub_category"] = response.css('ul.breadcrumbs a.breadcrumbs__link span::text').getall()[2]
        product_item["product_code"] = product.css('div.accordion strong:contains("Prekės kodas")').xpath('following-sibling::text()[1]').get()
        product_item["base_price"] = product.css('div.single-product__price span::text').get()
        product_item["old_price"] = product.css('div.single-product__price-regular div.price-val::text').get()
        product_item["conditional_discount_price"] = product.css('div.single-product__price span::text').get()
        product_item["discount_condition"] =  product.css('div.single-product__discount-message div::text').get()
        product_item["gintarine_conditional_discount"] = gintarine_discount_percentage
        product_item["source"] = "gintarine"

        yield product_item

#gintarine_discount_percentage = response.css('div.ribbons div.ribbon::text').get()
