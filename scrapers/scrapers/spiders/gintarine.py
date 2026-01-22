import scrapy
from scrapers.items import ProductItem

class GintarineSpider(scrapy.Spider):
    name = "gintarine"
    allowed_domains = ["www.gintarine.lt"]
    start_urls = ["https://www.gintarine.lt/akcijos-4"]

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
        # Current price with discount or without discount if there are conditions
        base_price = product.css('div.single-product__price span::text').get()
        # Price before discount (no conditions)
        old_price = product.css('div.single-product__price-regular div.price-val::text').get()
        # Price with discount if conditions are applied
        conditional_discount_price = product.css('div.single-product__price span::text').get()
        # Conditions of the discount
        discount_condition = product.css('div.single-product__bundle-message div::text').get()

        has_condition = bool(discount_condition)

        has_condition = bool(discount_condition)

        if has_condition:
            discount_type = "conditional"
            final_price = (
                    conditional_discount_price
                    or base_price
                    or old_price
            )

        elif base_price and old_price:
            discount_type = "direct"
            final_price = base_price

        else:
            discount_type = None
            final_price = base_price or old_price

        product_item = ProductItem()
        product_item["url"] = response.url
        product_item["title"] = product.css('h1.single-product__title::text').get()
        product_item["company_name"] = product.css('div.single-product__brand a::text').get()
        product_item["category"] = response.css('ul.breadcrumbs a.breadcrumbs__link span::text').getall()[1]
        product_item["product_code"] = product.css('div.accordion strong:contains("Prekės kodas")').xpath('following-sibling::text()[1]').get()
        product_item["base_price"] = base_price
        product_item["old_price"] = old_price
        product_item["conditional_discount_price"] = conditional_discount_price
        product_item["final_price"] = final_price
        product_item["discount_type"] = discount_type
        product_item["discount_condition"] = discount_condition
        product_item["source"] = "gintarine"
        yield product_item


