{{ config(materialized='view', schema="gold") }}

WITH industry_data AS (
    SELECT *
    FROM {{ ref('sp500_companies_tech_silver') }}
    UNION ALL
    SELECT *
    FROM {{ ref('sp500_companies_indus_silver') }}
    UNION ALL
    SELECT *
    FROM {{ ref('sp500_companies_health_silver') }}
    UNION ALL
    SELECT *
    FROM {{ ref('sp500_companies_finance_silver') }}
    UNION ALL
    SELECT *
    FROM {{ ref('sp500_companies_consumer_silver') }}
)

SELECT 
    industry,
    SUM(marketcap) AS total_marketcap,
    AVG(marketcap) AS avg_marketcap,
    SUM(revenuegrowth) AS total_revenuegrowth,
    AVG(revenuegrowth) AS avg_revenuegrowth,
    SUM(ebitda) AS total_ebitda,
    AVG(ebitda) AS avg_ebitda,
    SUM(fulltimeemployees) AS total_employees,
    AVG(fulltimeemployees) AS avg_employees
FROM 
    industry_data
GROUP BY 
    industry;
