-- Kiek kiekviena kategorija turi prekių

CREATE VIEW V_CatItems AS
SELECT
	mapped_categories,
	COUNT(*) AS 'Total Items Per Category'
FROM
	pharmacy_prices_clean.pharmacy_prices_clean
GROUP BY
	mapped_categories;
    
-- Kiek kiekviena vaistinė turi prekių kiekvienoje kategorijoje
    
CREATE VIEW V_CatItemsSource AS
SELECT
	mapped_categories,
    source,
	COUNT(*) AS 'Total Items Per Category'
FROM
	pharmacy_prices_clean.pharmacy_prices_clean
GROUP BY
	mapped_categories, source;
    
-- Kategorijų vidutinės, minimalios ir maksimalios kainos

CREATE VIEW V_AvgMaxMinCat AS
SELECT
	mapped_categories AS 'Categories',
	ROUND(AVG(final_price_equivalent), 2) AS 'Average Price',
    MIN(final_price_equivalent) AS 'Minimal Price',
    MAX(final_price_equivalent) AS 'Maximum price',
    COUNT(*) AS 'Total Number of Items'
FROM
	pharmacy_prices_clean.pharmacy_prices_clean
GROUP BY
	mapped_categories;
    
-- Vaistinių vidutinės, minimalios ir maksimalios kainos per kategorijas

CREATE VIEW V_AvgMaxMinCatPhar AS
SELECT
	mapped_categories AS 'Categories',
    source AS 'Pharmacy',
	ROUND(AVG(final_price_equivalent), 2) AS 'Average Price',
    MIN(final_price_equivalent) AS 'Minimal Price',
    MAX(final_price_equivalent) AS 'Maximum price',
    COUNT(*) AS 'Total Number of Items'
FROM
	pharmacy_prices_clean.pharmacy_prices_clean
GROUP BY
	mapped_categories, source;
    
-- Nuolaidų modelių pasiskirstymas per vaistines

CREATE VIEW V_DiscModelPhar AS
SELECT 
	source AS 'Pharmacy',
    discount_model AS 'Discount Model',
    COUNT(*) AS 'Total Number of Items'
FROM
	pharmacy_prices_clean.pharmacy_prices_clean
GROUP BY
	discount_model, source;

-- Nuolaidų modelių vidutinės, maksimalios ir minimalios kainos per vaistines

CREATE VIEW V_DiscModelPharPrice AS
SELECT 
	source AS 'Pharmacy',
    discount_model AS 'Discount Model',
    ROUND(AVG(final_price_equivalent), 2) AS 'Average Price Per Model',
    MAX(final_price_equivalent) AS 'Maximum Price Per Model',
    MIN(final_price_equivalent) AS 'Minimum Price Per Model',
    COUNT(*) AS 'Total Number of Items'
FROM
	pharmacy_prices_clean.pharmacy_prices_clean
GROUP BY
	discount_model, source;
    
-- Įmonių vidutinės, minimalios ir maksimalios kainos

CREATE VIEW V_BrandPrice AS
SELECT 
	company_name AS 'Company Name',
	ROUND(AVG(final_price_equivalent), 2) AS 'Average Price Per Model',
    MAX(final_price_equivalent) AS 'Maximum Price Per Model',
    MIN(final_price_equivalent) AS 'Minimum Price Per Model',
    COUNT(*) AS 'Total Number of Items'
FROM
	pharmacy_prices_clean.pharmacy_prices_clean
GROUP BY
	company_name;

-- Įmonių vidutinės, minimalios ir maksimalios kainos per vaistines

CREATE VIEW V_SimilarBrandPrice AS
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
	company_name, source;
    
-- Nuolaidos išraiša EUR per kiekvieną kategoriją, nuolaidos tipą vaistinėse

CREATE VIEW V_RealDiscountAll AS
SELECT 
	source AS 'Pharmacy Name',
	ROUND(AVG(old_price - final_price_equivalent), 2) AS 'Average Discount',
    ROUND(AVG(old_price), 2) AS 'Average Price Without Discount',
    mapped_categories AS 'Item Category',
    discount_model AS 'Discount Model'
FROM
	pharmacy_prices_clean.pharmacy_prices_clean
WHERE
	base_price IS NOT NULL AND old_price IS NOT NULL
GROUP BY
	source, mapped_categories, discount_model;
    
-- Vidutinės įmonių prekių kainos

CREATE VIEW V_AvgPricePerBrand AS
SELECT
	company_name AS 'Company Name',
    ROUND(AVG(final_price_equivalent), 2) AS 'Average Item Price',
    mapped_categories AS 'Item Category',
    COUNT(*) AS 'Total Number Of Items'
FROM
	pharmacy_prices_clean.pharmacy_prices_clean
WHERE
	company_name IS NOT NULL
GROUP BY
	company_name, mapped_categories;
    
-- Visų prekių kainų diapozonas

CREATE VIEW V_PriceRange AS
SELECT
	CASE
	WHEN final_price_equivalent < 5.00 THEN '< 5€'
	WHEN final_price_equivalent BETWEEN 5.01 AND 10.00 THEN '5€ - 10€'
	WHEN final_price_equivalent BETWEEN 10.01 AND 20.00 THEN '10€ - 20€'
	ELSE '> 20€'
    END AS 'Item Prise Range',
    COUNT(*) AS 'Total Number Of Items'
FROM
	pharmacy_prices_clean.pharmacy_prices_clean
GROUP BY
	`Item Prise Range`;
    
-- Prekių kainų diapozonas vaistinėse

CREATE VIEW V_PriceRangePharmacy AS
SELECT
	source AS 'Pharmacy Name',
	CASE
	WHEN final_price_equivalent < 5.00 THEN '< 5€'
	WHEN final_price_equivalent BETWEEN 5.01 AND 10.00 THEN '5€ - 10€'
	WHEN final_price_equivalent BETWEEN 10.01 AND 20.00 THEN '10€ - 20€'
	ELSE '> 20€'
    END AS 'Item Prise Range',
    COUNT(*) AS 'Total Number Of Items'
FROM
	pharmacy_prices_clean.pharmacy_prices_clean
GROUP BY
	`Item Prise Range`, source;
    
-- Kainų diapozonas per kategorijas

CREATE VIEW V_PriceRangeCategory AS
SELECT
	mapped_categories AS 'Category',
	CASE
	WHEN final_price_equivalent < 5.00 THEN '< 5€'
	WHEN final_price_equivalent BETWEEN 5.01 AND 10.00 THEN '5€ - 10€'
	WHEN final_price_equivalent BETWEEN 10.01 AND 20.00 THEN '10€ - 20€'
	ELSE '> 20€'
    END AS 'Item Prise Range',
    COUNT(*) AS 'Total Number Of Items'
FROM
	pharmacy_prices_clean.pharmacy_prices_clean
GROUP BY
	`Item Prise Range`, mapped_categories;