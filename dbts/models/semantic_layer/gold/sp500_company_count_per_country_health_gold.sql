{{ config(materialized='view', schema="gold") }}


SELECT Country, COUNT(*) AS Company_Count
FROM {{ ref('sp500_companies_health_silver') }}
GROUP BY Country;