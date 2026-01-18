import scrapy


class CameliaSpider(scrapy.Spider):
    name = "camelia"
    allowed_domains = ["camelia.lt"]
    start_urls = ["https://camelia.lt/akcijos"]



    if conditional_discount_price:
        discount_price = conditional_discount_price
        discount_type = "conditional"
    elif old_price:
        discount_price = base_price
        discount_type = "direct"
    else:
        discount_price = None
        discount_type = None

    def parse(self, response):
        products = response.css('div[data-test^="product-list-item"]')
        for product in products:
            relative_url = product.css('a[data-test^="product-card-link"]::attr(href)').get()
            full_url = respones.urljoin(relative_url)

            yield {
                'url': full_url,
                'name': product.css('div.product-name::text').get().strip(),
                'price': product.css('div.price::text').get(),}

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

        # Current price with discount or without discount if there are conditions
        base_price = product.css('div[data-test="product-price"] div[data-test="product-price-formatted"]::text').get()

        # Price before discount (no conditions)
        old_price = product.css('span[data-test^="product-price-original-item"]::text').get()

        # Price with discount if conditions are applied
        conditional_discount_price = product.css('span.discounted-price-value::text').get()

        # Conditions of the discount
        discount_condition = product.css('div.badge-content div::text').getall()
        discount_condition = " ".join(t.strip() for t in discount_condition if t.strip())

        company_name = product.css('a[href^="/a/prekes-zenklas/"]::text').get()

        yield {
            'name': product.css('div[data-test^="product-name"]::text').get(),
            'product_code':  product.css('div[data-test^="product-code"]::text').get(),

        }

        category = product.css('div.product-additional-info a::text').get()














