{{ config(materialized='view', schema="gold") }}

SELECT Date, volume
FROM {{ ref('sp500_stock_aapl_silver') }};