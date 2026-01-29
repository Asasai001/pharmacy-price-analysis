# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from dotenv import load_dotenv
import os
import mysql.connector
import re

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
            value = value.replace('\r\n', '')
            value = value.replace('€', ' ')
            adapter[field_name] = value

        codes = ['product_code']
        for code in codes:
          value = adapter.get(code)
          if value is not None:
            value = value.replace('prekės kodas:', '')
            value = value.strip()
            adapter[code] = value

        price_keys = ['base_price', 'old_price', 'conditional_discount_price']
        for price_key in price_keys:
          value = adapter.get(price_key)
          if value in (None, ''):
            adapter[price_key] = None
          else:
            value = value.replace(',', '.')
            adapter[price_key] = float(value)

        return item

class DiscountResolverPipeline:
    def process_item(self, item, spider):
        condition = item.get("discount_condition")

        if not condition:
            item["discount_model"] = "none"
            item["required_quantity"] = 1
            item["final_price_equivalent"] = item.get("base_price")
            return item

        # 1. nustatom modelį
        self.resolve_discount_model(item, condition)
        # 2. paskaičiuojam ekvivalentinę kainą
        self.calculate_equivalent_price(item)

        return item


    def resolve_discount_model(self, item, text):
        text = item.get("discount_condition")
        if not text:
            return item

        text = text.lower()

        # buy X get Y free
        if re.search(r'(nemokamai|dovanų|1+1)', text):
            item["discount_model"] = "buy_x_get_y"
            item["required_quantity"] = 2
            item["free_quantity"] = 1
            return item

        # second item percent
        match = re.search(r'(speciali kaina antrai|\d+)\s*%\s+antrai', text)
        if match:
            item["discount_model"] = "second_item_percent"
            item["required_quantity"] = 2
            item["second_item_discount_percent"] = int(match.group(1))
            return item

        # bulk minimum quantity
        match = re.search(r'(bent|ne mažiau nei)\s+(\d+)', text)
        if match:
            item["discount_model"] = "bulk_min_qty"
            item["required_quantity"] = int(match.group(2))
            return item

        # unknown conditional
        item["discount_model"] = "unknown_conditional"

    def calculate_equivalent_price(self, item):
        model = item.get("discount_model")

        if item.get("source") == "manovasitine":
            regular = item.get("old_price")
            conditional = item.get("conditional_discount_price")

            if model == "buy_x_get_y":
                total = regular * (item["required_quantity"] - item["free_quantity"])
                item["final_price_equivalent"] = total / item["required_quantity"]
            elif model == "second_item_percent":
                discount = item["second_item_discount_percent"]/100
                total = regular + (regular * (1 - discount))
                item["final_price_equivalent"] = total/2
            elif model == "bulk_min_qty":
                item["final_price_equivalent"] = conditional
            else:
                item["final_price_equivalent"] = None

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
        sub_category VARCHAR(80),
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
                sub_category,
                product_code,
                base_price,
                old_price,
                conditional_discount_price,
                final_price,
                discount_type,
                discount_condition,
                source
            )
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """,
            (
                item.get("url"),
                item.get("title"),
                item.get("company_name"),
                item.get("category"),
                item.get("sub_category"),
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

