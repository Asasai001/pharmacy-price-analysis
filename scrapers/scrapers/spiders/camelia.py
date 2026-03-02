import scrapy
from scrapers.items import ProductItem


class CameliaSpider(scrapy.Spider):
    name = "camelia"
    allowed_domains = ["camelia.lt"]
    start_urls = ["https://camelia.lt/akcijos"]


    custom_settings = {
        'FEEDS': {
            'camelia_data.json': {
                'format': 'json',
                'overwrite': True,
                'encoding': 'utf-8'
            }
        }
    }

    def parse(self, response):
        products = response.css('div[data-test^="product-list-item"]')
        for product in products:
            relative_url = product.css('a[data-test^="product-card-link"]::attr(href)').get()
            full_url = response.urljoin(relative_url)
            yield scrapy.Request(full_url, callback=self.parse_product_page)


        current_page = response.meta.get("page", 1)
        next_page = current_page + 1

        if next_page <= 121:
            next_url = f"https://camelia.lt/akcijos?page={next_page}"
            yield response.follow(
                next_url,
                callback=self.parse,
                meta={"page": next_page},
            )

    def parse_product_page(self, response):
        product = response.css("div.product-grid")
        product_item = ProductItem()

        breadcrumbs = response.css('ul.v-breadcrumbs li a::text').getall()

        old_price = product.css('span[data-test^="product-price-original-item"]::text').get()
        if old_price is None:
            old_price = product.css('div.price-value::text').get()

        product_item["url"] = response.url
        product_item["title"] = product.css('h1[data-test="product-name"]::text').get()
        product_item["company_name"] = product.css('a[href^="/a/prekes-zenklas/"]::text').get()
        product_item["category"] = product.css('div.product-additional-info a::text').get()
        product_item["sub_category"] = breadcrumbs[3] if len(breadcrumbs) > 3 else None
        product_item["product_code"] = product.css('div[data-test^="product-code"]::text').get()
        product_item["base_price"] = product.css('div[data-test="product-price"] div[data-test="product-price-formatted"]::text').get()
        product_item["old_price"] = old_price
        product_item["conditional_discount_price"] = product.css('span.discounted-price-value::text').get()
        product_item["discount_condition"] = " ".join(product.css('div.badge-content div::text').getall())
        product_item["direct_discount_raw"] = product.css('div.badge-percent span::text').get()
        product_item["conditional_discount_raw"] = product.css("li[data-test^='product-card-discount-0'] div::text").get()
        product_item["source"] = "camelia"

        yield product_item














