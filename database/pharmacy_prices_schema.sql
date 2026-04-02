-- Category mapping schema

CREATE TABLE category_mapping (
	original_name VARCHAR(255),
    mapped_category VARCHAR(100)
    );
    
-- Pharmacy prices schema

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