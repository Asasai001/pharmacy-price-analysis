from load_data import load_query

def discount_model_pharmacy():
    query = """
    SELECT 
	    source AS 'Pharmacy',
        discount_model AS 'Discount Model',
        COUNT(*) AS 'Total Number of Items'
    FROM
	    pharmacy_prices_clean.pharmacy_prices_clean
    GROUP BY
	    discount_model, source
    ORDER BY
	    discount_model;
    """
    return load_query(query)

#Avg kainos skirtumas tarp senos kainos ir siulomos per nuolaidos kategorijas

def bulk_min_qty():
    query = """
    SELECT 
	    source AS 'Pharmacy Name',
	    ROUND(AVG(old_price - final_price_equivalent), 2) AS 'Average Discount',
        ROUND(AVG(old_price), 2) AS 'Average Price Without Discount',
        mapped_categories AS 'Item Category',
        discount_model AS 'Discount Model'
    FROM
	    pharmacy_prices_clean.pharmacy_prices_clean
    WHERE
	    base_price IS NOT NULL AND old_price IS NOT NULL AND discount_model = 'bulk_min_qty'
    GROUP BY
	    source, mapped_categories, discount_model
    ORDER BY
	    source, mapped_categories, discount_model;
	"""
    return load_query(query)


def direct_percent():
    query = """
    SELECT 
	    source AS 'Pharmacy Name',
	    ROUND(AVG(old_price - final_price_equivalent), 2) AS 'Average Discount',
        ROUND(AVG(old_price), 2) AS 'Average Price Without Discount',
        mapped_categories AS 'Item Category',
        discount_model AS 'Discount Model'
    FROM
	    pharmacy_prices_clean.pharmacy_prices_clean
    WHERE
	    base_price IS NOT NULL AND old_price IS NOT NULL AND discount_model = 'direct_percent'
    GROUP BY
	    source, mapped_categories, discount_model
    ORDER BY
	    source, mapped_categories, discount_model;
	"""
    return load_query(query)


def buy_x_get_y():
    query = """
        SELECT 
    	    source AS 'Pharmacy Name',
    	    ROUND(AVG(old_price - final_price_equivalent), 2) AS 'Average Discount',
            ROUND(AVG(old_price), 2) AS 'Average Price Without Discount',
            mapped_categories AS 'Item Category',
            discount_model AS 'Discount Model'
        FROM
    	    pharmacy_prices_clean.pharmacy_prices_clean
        WHERE
    	    base_price IS NOT NULL AND old_price IS NOT NULL AND discount_model = 'buy_x_get_y'
        GROUP BY
    	    source, mapped_categories, discount_model
        ORDER BY
    	    source, mapped_categories, discount_model;
    	"""
    return load_query(query)


def run_discount_analysis():
    model = discount_model_pharmacy()
    min_qty = bulk_min_qty()
    direct = direct_percent()
    buy_get = buy_x_get_y()
    return model, min_qty, direct, buy_get




#if __name__ == "__main__":
 #   df = buy_x_get_y()
  #  print(df)
