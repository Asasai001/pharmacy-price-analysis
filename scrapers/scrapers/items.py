# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapersItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class ProductItem(scrapy.Item):
   url = scrapy.Field()
   title = scrapy.Field()
   company_name = scrapy.Field()
   category = scrapy.Field()
   sub_category = scrapy.Field()
   product_code = scrapy.Field()
   base_price = scrapy.Field()
   old_price = scrapy.Field()
   conditional_discount_price = scrapy.Field()
   discount_condition = scrapy.Field()
   direct_discount = scrapy.Field()
   conditional_discount = scrapy.Field()
   source = scrapy.Field()
   discount_model = scrapy.Field()
   required_quantity = scrapy.Field()
   free_quantity = scrapy.Field()
   second_item_discount_percent = scrapy.Field()
   final_price_equivalent = scrapy.Field()
   bulk_discount_percent = scrapy.Field()
   direct_discount_percent = scrapy.Field()


""" from gintarine
class ProductItem(scrapy.Item):
   url = scrapy.Field()
   title = scrapy.Field()
   company_name = scrapy.Field()
   category = scrapy.Field()
   sub_category = scrapy.Field()
   product_code = scrapy.Field()
   base_price = scrapy.Field()
   old_price = scrapy.Field()
   conditional_discount_price = scrapy.Field()
   discount_condition = scrapy.Field()
   gintarine_direct_discount = scrapy.Field()
   gintarine_conditional_discount = scrapy.Field()
   source = scrapy.Field()
   discount_model = scrapy.Field()
   required_quantity = scrapy.Field()
   free_quantity = scrapy.Field()
   second_item_discount_percent = scrapy.Field()
   bulk_discount_percent = scrapy.Field()
   direct_discount_percent = scrapy.Field()
   final_price_equivalent = scrapy.Field()"""
