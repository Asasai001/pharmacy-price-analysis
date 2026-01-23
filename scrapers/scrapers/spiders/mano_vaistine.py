import scrapy


class ManoVaistineSpider(scrapy.Spider):
    name = "mano_vaistine"
    allowed_domains = ["www.manovaistine.lt"]
    start_urls = ["https://www.manovaistine.lt/akcijos?_gl=1"]

    def parse(self, response):
        products = response.css('main.body')
        for product in products:
            relative_url = product.css('div.item-title a::attr(href)').get()
            full_url = response.urljoin(relative_url)
            yield scrapy.Request(url=full_url, callback=self.parse_product_page)


        current_page = response.meta.get("page", 1)
        next_page = current_page + 1

        if next_page <= 152:
            next_url = f"https://www.manovaistine.lt/akcijos?_gl={next_page}"
            yield response.follow(
                next_url,
                callback=self.parse,
                meta={"page": next_page},
            )

product = response.css('div.product')
title = product.css('div.product-title h1::text').get()
company_name = product.css('div a.product-brand-link::text').get()
product_code = product.css('dl.product-attributes span.product-attribute-value::text').get()
old_price = product.css('span.product-price::text').get()
base_price = product.css('div.product-inner-loyalty-container--special-price-amount::text').get()
conditional_discount_price = product.css('div.product-inner-pan-special-price::text').get()
discount_condition = product.css('li.plus-promo-info-text::text').get()
category = response.css('li.breadcrumb-item a[href]::text').getall()[1]
sub_category = response.css('li.breadcrumb-item a[href]::text').getall()[2]
source = 'manovasitine'