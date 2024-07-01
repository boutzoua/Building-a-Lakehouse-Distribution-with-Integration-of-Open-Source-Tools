{{ config(materialized='view', schema="gold") }}

SELECT AVG(sp500) AS Avg_SP500
FROM {{ ref('sp500_index_silver') }};