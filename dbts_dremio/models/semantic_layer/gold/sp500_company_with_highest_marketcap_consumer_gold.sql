{{ config(materialized='view', schema="Data Analytics.gold") }}

SELECT Symbol, Shortname, Marketcap
FROM {{ ref('sp500_companies_consumer_silver') }}
ORDER BY Marketcap DESC
LIMIT 10;