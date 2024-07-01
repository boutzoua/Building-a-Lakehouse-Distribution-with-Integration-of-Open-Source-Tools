{{ config(materialized='view', schema="Data Analytics.silver") }}

WITH stock_data AS (
    SELECT
        "date",
        adj_close,
        "close",
        high,
        low,
        "open",
        volume,
        LAG(adj_close) OVER (ORDER BY "date") AS prev_adj_close,
        LAG("close") OVER (ORDER BY "date") AS prev_close,
        LAG(high) OVER (ORDER BY "date") AS prev_high,
        LAG(low) OVER (ORDER BY "date") AS prev_low,
        LAG("open") OVER (ORDER BY "date") AS prev_open,
        LAG(volume) OVER (ORDER BY "date") AS prev_volume
    FROM {{ ref('sp500_stock_bronze') }}
)

SELECT
    "date",
    COALESCE(adj_close, prev_adj_close) AS adj_close,
    COALESCE("close", prev_close) AS "close",
    COALESCE(high, prev_high) AS high,
    COALESCE(low, prev_low) AS low,
    COALESCE("open", prev_open) AS "open",
    COALESCE(volume, prev_volume) AS volume
FROM stock_data;
