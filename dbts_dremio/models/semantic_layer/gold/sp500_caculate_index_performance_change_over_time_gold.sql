{{ config(materialized='view' , schema='Data Analytics.gold') }}

SELECT "Date", sp500 - LAG(sp500) OVER (ORDER BY "Date") AS Index_Change
FROM {{ ref('sp500_index_silver') }};