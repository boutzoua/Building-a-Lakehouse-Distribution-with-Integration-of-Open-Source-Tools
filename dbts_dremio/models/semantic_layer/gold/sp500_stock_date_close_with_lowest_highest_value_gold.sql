{{ config(materialized='view', schema="Data Analytics.gold") }}

WITH highest_value AS (
    SELECT "date",  adj_close
    FROM {{ ref('sp500_stock_aapl_silver') }}
    ORDER BY adj_close DESC
    LIMIT 1
),
lowest_value AS (
    SELECT "date", adj_close
    FROM {{ ref('sp500_stock_aapl_silver') }}
    ORDER BY adj_close
    LIMIT 1
)

SELECT hv.adj_close as highest,
       lv.adj_close as lowest,
       hv."date" AS highest_date,
        lv."date" AS lowest_date
    FROM 
        highest_value AS hv 
    CROSS JOIN 
        lowest_value AS lv;
    