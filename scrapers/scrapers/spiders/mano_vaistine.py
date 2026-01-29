import scrapy
from scrapers.items import ProductItem


class ManoVaistineSpider(scrapy.Spider):
    name = "mano_vaistine"
    allowed_domains = ["www.manovaistine.lt"]
    start_urls = ["https://www.manovaistine.lt/akcijos?_gl=1"]


    custom_settings = {
        'FEEDS': {
            'manovaistine_data.json': {
                'format': 'json',
                'overwrite': True,
                'encoding': 'utf-8'
            }
        }
    }

    def parse(self, response):
        products = response.css('article.item.custom-grid-item')
        for product in products:
            relative_url = product.css('div.item-title a::attr(href)').get()
            full_url = response.urljoin(relative_url)
            yield scrapy.Request(url=full_url, callback=self.parse_product_page)


        current_page = response.meta.get("page", 1)
        next_page = current_page + 1

        if next_page <= 152:
            next_url = f"https://www.manovaistine.lt/akcijos/{next_page}"
            yield response.follow(
                next_url,
                callback=self.parse,
                meta={"page": next_page},
            )

    def parse_product_page(self, response):
        product = response.css('div.product')
        breadcrumbs = response.css('li.breadcrumb-item a[href]::text').getall()

        product_item = ProductItem()

        product_item["url"] = response.url
        product_item["title"] = product.css('div.product-title h1::text').get()
        product_item["company_name"] = product.css('div a.product-brand-link::text').get()
        product_item["category"] = breadcrumbs[1] if len(breadcrumbs) > 1 else None
        product_item["sub_category"] = breadcrumbs[2] if len(breadcrumbs) > 2 else None
        product_item["product_code"] = product.css('dl.product-attributes span.product-attribute-value::text').get()
        product_item["base_price"] = product.css('div.product-inner-loyalty-container--special-price-amount::text').get()
        product_item["old_price"] = product.css('span.product-price::text').get()
        product_item["conditional_discount_price"] = product.css('div.product-inner-pan-special-price::text').get()
        product_item["discount_condition"] = product.css('li.plus-promo-info-text::text').get()
        product_item["manovaistine_direct_discount"] = product.css('div.item-voucher-blob-text::text').get()
        product_item["manovaistine_conditional_discount"] = product.css('div.item-voucher-blob-text span').xpath('following-sibling::text()[1]').get()
        product_item["source"] = "manovasitine"

        yield product_item


#product = response.css('div.product')
#title = product.css('div.product-title h1::text').get()
#company_name = product.css('div a.product-brand-link::text').get()
#product_code = product.css('dl.product-attributes span.product-attribute-value::text').get()
#old_price = product.css('span.product-price::text').get()
#base_price = product.css('div.product-inner-loyalty-container--special-price-amount::text').get()
#conditional_discount_price = product.css('div.product-inner-pan-special-price::text').get()
#discount_condition = product.css('li.plus-promo-info-text::text').get()
#category = response.css('li.breadcrumb-item a[href]::text').getall()[1]
#sub_category = response.css('li.breadcrumb-item a[href]::text').getall()[2]
#source = 'manovasitine'

#product_item['mano_vaistine_conditional_price'] = product.css('li.plus-promo-info-text div::text').get()
#manovaistine_direct_discount = product.css('div.item-voucher-blob-text::text').get()
#manovaistine_conditional_discount = product.css('div.item-voucher-blob-text span').xpath('following-sibling::text()[1]').get()