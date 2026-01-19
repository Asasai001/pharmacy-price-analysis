# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from dotenv import load_dotenv
import os
import mysql.connector

load_dotenv()

class ScrapersPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        field_names = adapter.field_names()
        for field_name in field_names:
          value = adapter.get(field_name)
          if isinstance(value, str):
            value = value.strip().lower()
            value = value.replace('\xa0€', '')
            value = value.replace('\u00a0', ' ')
            adapter[field_name] = value

        codes = ['product_code']
        for code in codes:
          value = adapter.get(code)
          if value is not None:
            value = value.replace('prekės kodas:', '')
            value = value.strip()
            adapter[code] = value

        price_keys = ['base_price', 'old_price', 'conditional_discount_price', 'final_price']
        for price_key in price_keys:
          value = adapter.get(price_key)
          if value in (None, ''):
            adapter[price_key] = None
          else:
            value = value.replace(',', '.')
            adapter[price_key] = float(value)

        return item

class SaveToMySQLPipeline:

    def __init__(self):
        self.conn = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
            port=os.getenv("DB_PORT"),
        )

        self.cur = self.conn.cursor()

        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS pharmacy_prices(
        id int NOT NULL auto_increment,
        url VARCHAR(255),
        title TEXT,
        company_name VARCHAR(60),
        category VARCHAR(80),
        product_code VARCHAR(30),
        base_price DECIMAL(10,2),
        old_price DECIMAL(10,2),
        conditional_discount_price DECIMAL(10,2),
        final_price DECIMAL(10,2),
        discount_type VARCHAR(30),
        discount_condition VARCHAR(255),
        source VARCHAR(40),
        PRIMARY KEY (id)
        )
        """)

    def process_item(self, item, spider):
        self.cur.execute(
            """
            INSERT INTO pharmacy_prices (
                url,
                title,
                company_name,
                category,
                product_code,
                base_price,
                old_price,
                conditional_discount_price,
                final_price,
                discount_type,
                discount_condition,
                source
            )
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """,
            (
                item.get("url"),
                item.get("title"),
                item.get("company_name"),
                item.get("category"),
                item.get("product_code"),
                item.get("base_price"),
                item.get("old_price"),
                item.get("conditional_discount_price"),
                item.get("final_price"),
                item.get("discount_type"),
                item.get("discount_condition"),
                item.get("source"),
            )
        )
        self.conn.commit()
        return item

    def close_spider(self, spider):
        self.cur.close()
        self.conn.close()

