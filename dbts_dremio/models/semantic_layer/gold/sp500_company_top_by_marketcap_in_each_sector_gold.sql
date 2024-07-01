{{ config(materialized='view', schema="Data Analytics.gold") }}

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
),

ranked_companies AS (
    SELECT
        *,
        ROW_NUMBER() OVER (PARTITION BY industry ORDER BY marketcap DESC) AS company_rank
    FROM
        industry_data
)

SELECT 
    industry,
    symbol,
    shortname,
    marketcap
FROM 
    ranked_companies
WHERE 
    company_rank <= 3;
