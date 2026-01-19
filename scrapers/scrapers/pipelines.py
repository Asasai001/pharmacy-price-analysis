# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class ScrapersPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        field_names = adapter.field_names()
        for field_name in field_names:
          value = adapter.get(field_name)
          if isinstance(value, str):
            value = value.strip().lower()
            value = value.replace('\xa0€', '')
            adapter[field_name] = value

        price_keys = ['base_price', 'old_price', 'conditional_discount_price', 'final_price']
        for price_key in price_keys:
          value = adapter.get(price_key)
          if value in (None, ''):
            adapter[price_key] = None
          else:
            value = value.replace(',', '.')
            adapter[price_key] = float(value)


        return item
