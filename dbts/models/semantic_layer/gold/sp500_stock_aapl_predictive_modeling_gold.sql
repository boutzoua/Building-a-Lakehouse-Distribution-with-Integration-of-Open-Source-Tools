{{ config(materialized='view', schema="datascience") }}

-- Train machine learning models using historical stock data
SELECT
    s.date,
    s.adj_close,
    s.volume,
    LAG(s.adj_close) OVER (ORDER BY s.date) AS prev_adj_close,
    LAG(s.volume) OVER (ORDER BY s.date) AS prev_volume
FROM
    {{ ref('sp500_stock_aapl_silver') }} AS s;
