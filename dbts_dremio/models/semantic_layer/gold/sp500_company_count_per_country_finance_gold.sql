{{ config(materialized='view', schema="Data Analytics.gold") }}

SELECT Country, COUNT(*) AS Company_Count
FROM {{ ref('sp500_companies_finance_silver') }}
GROUP BY Country;