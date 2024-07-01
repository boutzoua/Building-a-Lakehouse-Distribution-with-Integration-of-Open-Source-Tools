{{ config(materialized='view', schema="gold") }}

SELECT Country, COUNT(*) AS Company_Count
FROM {{ ref('sp500_companies_tech_silver') }}
GROUP BY country;