{{ config(materialized='view', schema="silver") }}

SELECT
    COUNT(*) AS null_count_adj_close,
    COUNT(*) AS null_count_close,
    COUNT(*) AS null_count_high,
    COUNT(*) AS null_count_low,
    COUNT(*) AS null_count_open,
    COUNT(*) AS null_count_volume
FROM
    {{ ref('sp500_stock_bronze') }}
WHERE
    adj_close IS NULL
    OR close IS NULL
    OR high IS NULL
    OR low IS NULL
    OR open IS NULL
    OR volume IS NULL;