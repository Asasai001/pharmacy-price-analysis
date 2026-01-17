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

        current_page = response.meta.get("page", 1)
        next_page = current_page + 1

        if next_page <= 121:
            next_url = f"https://camelia.lt/akcijos?page={next_page}"
            yield response.follow(
                next_url,
                callback=self.parse,
                meta={"page": next_page}
            )


