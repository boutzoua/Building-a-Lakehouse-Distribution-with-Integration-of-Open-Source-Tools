{{ config(materialized='view' , schema='gold') }}

SELECT Date, sp500 - LAG(sp500) OVER (ORDER BY Date) AS Index_Change
FROM {{ ref('sp500_index_silver') }};