{{ config(materialized='view', schema='gold' ) }}


SELECT Date, (adj_close - LAG(adj_close) OVER (ORDER BY Date)) / LAG(adj_close) OVER (ORDER BY Date) AS Return
FROM {{ ref('sp500_stock_aapl_silver') }};