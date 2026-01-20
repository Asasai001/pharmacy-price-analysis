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

