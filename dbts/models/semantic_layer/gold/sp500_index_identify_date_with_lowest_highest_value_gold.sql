{{ config(materialized='view', schema="gold") }}

WITH highest_value AS (
    SELECT date, sp500
    FROM {{ ref('sp500_index_silver') }}
    ORDER BY sp500 DESC
    LIMIT 1
),
lowest_value AS (
    SELECT date, sp500
    FROM {{ ref('sp500_index_silver') }}
    ORDER BY sp500
    LIMIT 1
)

SELECT hv.sp500 as highest,
        lv.sp500 as lowest,
        hv.date AS highest_date,
        lv.date AS lowest_date
    FROM 
        highest_value AS hv 
    CROSS JOIN 
        lowest_value AS lv;
    