{{ config(materialized='view', schema="Data Analytics.gold") }}

SELECT "Date", volume
FROM {{ ref('sp500_stock_aapl_silver') }};