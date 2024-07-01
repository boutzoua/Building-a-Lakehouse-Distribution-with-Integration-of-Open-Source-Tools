{{ config(materialized='view', schema="Data Analytics.silver") }}

WITH column_averages AS (
    SELECT
        AVG(sp500) AS avg_sp500
    FROM {{ ref('sp500_index_bronze') }}
)

SELECT 
    bi."date",
    COALESCE(bi.sp500, ca.avg_sp500) AS sp500
FROM {{ ref('sp500_index_bronze') }} as bi, column_averages as ca
