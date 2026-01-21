import scrapy


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
            next_url = f"https://camelia.lt/akcijos-4?pagenumber={next_page}"
            yield response.follow(
                next_url,
                callback=self.parse,
                meta={"page": next_page},
            )

#product = response.css('main.single-product')
#base_price = product.css('div.single-product__price span::text').get()
#title = product.css('h1.single-product__title::text').get()
#company_name = product.css('div.single-product__brand a::text').get()
#category = response.css('ul.breadcrumbs a.breadcrumbs__link span::text').getall()[1]
#product_code = product.css('div.accordion strong:contains("Prekės kodas")').xpath('following-sibling::text()[1]').get()
#old_price = product.css('div.single-product__price-regular div.price-val::text').get()
#discount_condition = product.css('div.single-product__bundle-message div::text').get()

