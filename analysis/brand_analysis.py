from analysis.load_data import load_query

#Brand avg kainos
def brand_avg_price():
    query = """
    SELECT 
	    company_name AS 'Company Name',
	    ROUND(AVG(final_price_equivalent), 2) AS 'Average Price Per Model',
        MAX(final_price_equivalent) AS 'Maximum Price Per Model',
        MIN(final_price_equivalent) AS 'Minimum Price Per Model',
        COUNT(*) AS 'Total Number of Items'
    FROM
	    pharmacy_prices_clean.pharmacy_prices_clean
    GROUP BY
	    company_name
    ORDER BY
	    COUNT(*) DESC;
    """
    return load_query(query)


#Brand avg kainos per vaistines

def brand_avg_pharm():
    query = """
    SELECT 
	    source AS 'Pharmacy',
	    company_name AS 'Company Name',
	    ROUND(AVG(final_price_equivalent), 2) AS 'Average Price Per Model',
        MAX(final_price_equivalent) AS 'Maximum Price Per Model',
        MIN(final_price_equivalent) AS 'Minimum Price Per Model',
        COUNT(*) AS 'Total Number of Items'
    FROM
	    pharmacy_prices_clean.pharmacy_prices_clean
    WHERE company_name IN
	    (select company_name
        from pharmacy_prices_clean.pharmacy_prices_clean
        group by company_name
        having count(distinct source) > 1
        )
    GROUP BY
	    company_name, source
    ORDER BY
	    company_name;
	"""
    return load_query(query)


#Vidutines kainos per brand ir kategorija

def brand_cat_avg():
    query = """
    SELECT
	    company_name AS 'Company Name',
        ROUND(AVG(final_price_equivalent), 2) AS 'Average Item Price',
        mapped_categories AS 'Item Category',
        COUNT(*) AS 'Total Number Of Items'
    FROM
	    pharmacy_prices_clean.pharmacy_prices_clean
    WHERE
	    company_name IS NOT NULL AND final_price_equivalent IS NOT NULL
    GROUP BY
	    company_name, mapped_categories
    ORDER BY
	    company_name;
	"""
    return load_query(query)