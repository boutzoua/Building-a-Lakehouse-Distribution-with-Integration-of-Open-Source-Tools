{{ config(materialized='view', schema="gold") }}

SELECT
    s.date,
    s.adj_close AS stock_adj_close,
    i.sp500 AS index_sp500
FROM
    {{ ref('sp500_stock_aapl_silver') }} AS s
JOIN
    {{ ref('sp500_index_silver') }} AS i
ON
    s.date = i.date
ORDER BY
    s.date;