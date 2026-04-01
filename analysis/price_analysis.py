from analysis.load_data import load_query

# avg kainos per  kategorija
def avg_price_cat():
    query = """
    SELECT
	    mapped_categories AS 'Categories',
	    ROUND(AVG(final_price_equivalent), 2) AS 'Average Price',
        MIN(final_price_equivalent) AS 'Minimal Price',
        MAX(final_price_equivalent) AS 'Maximum price',
        COUNT(*) AS 'Total Number of Items'
    FROM
	    pharmacy_prices_clean.pharmacy_prices_clean
	WHERE 
	    final_price_equivalent IS NOT NULL
    GROUP BY
	    mapped_categories
    ORDER BY
	    mapped_categories;
    """
    return load_query(query)


#avg kainos per kategorijas vaistinese

def avg_cat_pharm():
    query = """
    SELECT
	    mapped_categories AS 'Categories',
        source AS 'Pharmacy',
	    ROUND(AVG(final_price_equivalent), 2) AS 'Average Price',
        MIN(final_price_equivalent) AS 'Minimal Price',
        MAX(final_price_equivalent) AS 'Maximum price',
        COUNT(*) AS 'Total Number of Items'
    FROM
	    pharmacy_prices_clean.pharmacy_prices_clean
	WHERE 
	    final_price_equivalent IS NOT NULL
    GROUP BY
	    mapped_categories, source
    ORDER BY
	    mapped_categories;
    """
    return load_query(query)


#Price range
def price_range():
    query = """
    SELECT
	    CASE
	    WHEN final_price_equivalent <= 4.99 THEN '< 5€'
	    WHEN final_price_equivalent BETWEEN 5.00 AND 10.00 THEN '5€ - 10€'
	    WHEN final_price_equivalent BETWEEN 10.01 AND 20.00 THEN '10€ - 20€'
	    ELSE '> 20€'
        END AS 'Item Price Range',
        COUNT(*) AS 'Total Number Of Items'
    FROM
	    pharmacy_prices_clean.pharmacy_prices_clean
	WHERE 
	    final_price_equivalent IS NOT NULL
    GROUP BY
	    `Item Price Range`
    ORDER BY
	    MIN(final_price_equivalent);
	"""
    return load_query(query)


#Price range per kategorijas
def price_range_cat():
    query = """
    SELECT
        source AS 'Pharmacy',
	    mapped_categories AS 'Category',
	    CASE
	    WHEN final_price_equivalent <= 4.99 THEN '< 5€'
	    WHEN final_price_equivalent BETWEEN 5.00 AND 10.00 THEN '5€ - 10€'
	    WHEN final_price_equivalent BETWEEN 10.01 AND 20.00 THEN '10€ - 20€'
	    ELSE '> 20€'
        END AS 'Item Price Range',
        COUNT(*) AS 'Total Number Of Items'
    FROM
	    pharmacy_prices_clean.pharmacy_prices_clean
	WHERE 
	    final_price_equivalent IS NOT NULL
    GROUP BY
	    `Item Price Range`, mapped_categories, source
    ORDER BY
	    MIN(final_price_equivalent);
	"""
    return load_query(query)


def price_range_sum():
    query = """
    SELECT
	source AS 'Pharmacy',
	mapped_categories AS 'Category',
	COUNT(*) AS 'Total Number Of Items',
	SUM(CASE WHEN final_price_equivalent < 5 THEN 1 ELSE 0 END) AS '< 5€',
	SUM(CASE WHEN final_price_equivalent BETWEEN 5 AND 10 THEN 1 ELSE 0 END) AS '5€ - 10€',
	SUM(CASE WHEN final_price_equivalent BETWEEN 10.01 AND 20 THEN 1 ELSE 0 END) AS '10€ - 20€',
	SUM(CASE WHEN final_price_equivalent > 20 THEN 1 ELSE 0 END) AS '> 20€'
FROM
	pharmacy_prices_clean.pharmacy_prices_clean
WHERE
	final_price_equivalent IS NOT NULL
GROUP BY
	source, mapped_categories
ORDER BY
	source, mapped_categories;
	"""
    return load_query(query)