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
        source = item.get("source")

        if source == "manovasitine":
            self.resolve_manovaistine(item)

        elif source == "gintarine":
            self.resolve_gintarine(item)

        elif source == "camelia":
            self.resolve_camelia(item)

        self.calculate_equivalent_price(item)
        return item

    def extract_percent(self, text):
        if not text:
            return None
        match = re.search(r'(\d+)', text)
        return int(match.group(1)) if match else None

    def resolve_manovaistine(self, item):
        text = (item.get("discount_condition") or "").lower()
        direct_raw = item.get("direct_discount_raw")
        direct_percent = self.extract_percent(direct_raw)


        if not text and not direct_percent:
            item["discount_model"] = "none"
            item["required_quantity"] = 1
            item["direct_discount_percent"] = None
            item["bulk_discount_percent"] = None
            return

        if re.search(r'(1\+1|nemokamai|dovanų)', text):
            item["discount_model"] = "buy_x_get_y"
            item["required_quantity"] = 2
            item["free_quantity"] = 1
            item["direct_discount_percent"] = None
            item["bulk_discount_percent"] = None
            return

        if "antrai" in text:
            percent = self.extract_percent(item.get("conditional_discount"))
            if percent:
                item["discount_model"] = "second_item_percent"
                item["required_quantity"] = 2
                item["second_item_discount_percent"] = percent
                item["direct_discount_percent"] = None
                item["bulk_discount_percent"] = None
                return

        match = re.search(r'bent\s+(\d+)', text)
        if match:
            item["discount_model"] = "bulk_min_qty"
            item["required_quantity"] = int(match.group(1))
            item["bulk_discount_percent"] = direct_percent
            item["direct_discount_percent"] = None
            return

        item["discount_model"] = "unknown_conditional"
        item["required_quantity"] = 1
        item["direct_discount_percent"] = None
        item["bulk_discount_percent"] = None

    def resolve_gintarine(self, item):
        message_raw = item.get("direct_discount_raw")
        ribbon_raw = item.get("conditional_discount_raw")
        message = (message_raw or "").lower()
        ribbon = (ribbon_raw or "").lower()
        combined = f"{message} {ribbon}"

        percent = self.extract_percent(ribbon) or self.extract_percent(message)

        if not message and not ribbon:
            item["discount_model"] = "none"
            item["required_quantity"] = 1
            item["direct_discount_percent"] = None
            item["bulk_discount_percent"] = None
            return

        if re.search(r'(2\s*u[zž]\s*1|dovan|nemokam|antra.*nemok)', combined):
            item["discount_model"] = "buy_x_get_y"
            item["required_quantity"] = 2
            item["free_quantity"] = 1
            item["direct_discount_percent"] = None
            item["bulk_discount_percent"] = None
            return

        match = re.search(r'perkant\s+(\d+)', combined)
        if match:
            qty = int(match.group(1))
            item["discount_model"] = "bulk_min_qty"
            item["required_quantity"] = qty
            item["bulk_discount_percent"] = percent
            item["direct_discount_percent"] = None
            return

        if percent:
            item["discount_model"] = "direct_percent"
            item["required_quantity"] = 1
            item["direct_discount_percent"] = percent
            item["bulk_discount_percent"] = None
            return

        item["discount_model"] = "unknown_conditional"
        item["required_quantity"] = 1
        item["direct_discount_percent"] = None
        item["bulk_discount_percent"] = None

    def resolve_camelia(self, item):
        text = (item.get("discount_condition") or "").lower()
        direct_raw = item.get("direct_discount_raw")
        direct_percent = self.extract_percent(direct_raw)

        if not text and not direct_percent :
            item["discount_model"] = "none"
            item["required_quantity"] = 1
            item["direct_discount_percent"] = None
            item["bulk_discount_percent"] = None
            return

        if re.search(r'(nemokamai|dovanų|1\+1)', text):
            item["discount_model"] = "buy_x_get_y"
            item["required_quantity"] = 2
            item["free_quantity"] = 1
            item["bulk_discount_percent"] = None
            item["direct_discount_percent"] = None
            return

        match = re.search(r'bent\s+(\d+)', text)
        if match:
            qty = int(match.group(1))
            item["discount_model"] = "bulk_min_qty"
            item["required_quantity"] = qty
            item["bulk_discount_percent"] = direct_percent
            item["direct_discount_percent"] = None
            return

        if direct_percent:
            item["discount_model"] = "direct_percent"
            item["required_quantity"] = 1
            item["direct_discount_percent"] = direct_percent
            item["bulk_discount_percent"] = None
            return

        item["discount_model"] = "unknown_conditional"
        item["required_quantity"] = 1
        item["direct_discount_percent"] = None
        item["bulk_discount_percent"] = None

    def calculate_equivalent_price(self, item):
        model = item.get("discount_model")
        regular = item.get("old_price")
        conditional = item.get("conditional_discount_price")

        if model == "buy_x_get_y" and regular is not None:
            total = regular * (item["required_quantity"] - item["free_quantity"])
            item["final_price_equivalent"] = round(total / item["required_quantity"], 2)
        elif model == "second_item_percent":
            discount = item["second_item_discount_percent"]/100
            total = regular + (regular * (1 - discount))
            item["final_price_equivalent"] = round(total / 2, 2)
        elif model == "bulk_min_qty":
            if conditional is not None:
                item["final_price_equivalent"] = conditional
            elif regular is not None and item.get("bulk_discount_percent") is not None:
                discount = item["bulk_discount_percent"] / 100
                item["final_price_equivalent"] = round(regular * (1 - discount), 2)
            else:
                item["final_price_equivalent"] = None
        elif model == "direct_percent":
            item["final_price_equivalent"] = item.get("base_price")
        elif model == "none":
            item["final_price_equivalent"] = item.get("base_price")
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
            autocommit = True,
        )

        self.cur = self.conn.cursor()

        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS pharmacy_prices(
        id INT NOT NULL AUTO_INCREMENT,
        url VARCHAR(255),
        title TEXT,
        company_name VARCHAR(60),
        category VARCHAR(80),
        sub_category VARCHAR(80),
        product_code VARCHAR(30),
        base_price DECIMAL(10,2),
        old_price DECIMAL(10,2),
        conditional_discount_price DECIMAL(10,2),
        discount_condition VARCHAR(255),
        discount_model VARCHAR(40),
        source VARCHAR(40),
        required_quantity INT,
        free_quantity INT,
        direct_discount_raw VARCHAR(255),
        conditional_discount_raw VARCHAR(255),
        direct_discount_percent INT,
        bulk_discount_percent INT,
        second_item_discount_percent INT,
        final_price_equivalent DECIMAL(10,2),
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
                discount_condition,
                discount_model,
                source,
                required_quantity,
                free_quantity,
                direct_discount_raw,
                conditional_discount_raw,
                direct_discount_percent,
                bulk_discount_percent,
                second_item_discount_percent,
                final_price_equivalent
            )
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
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
                item.get("discount_condition"),
                item.get("discount_model"),
                item.get("source"),
                item.get("required_quantity"),
                item.get("free_quantity"),
                item.get("direct_discount_raw"),
                item.get("conditional_discount_raw"),
                item.get("direct_discount_percent"),
                item.get("bulk_discount_percent"),
                item.get("second_item_discount_percent"),
                item.get("final_price_equivalent"),
            )
        )
        return item

    def close_spider(self, spider):
        self.conn.commit()
        self.cur.close()
        self.conn.close()
