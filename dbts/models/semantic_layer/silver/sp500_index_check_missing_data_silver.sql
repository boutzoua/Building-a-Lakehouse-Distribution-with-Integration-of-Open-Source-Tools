{{ config(materialized='view', schema="silver") }}

WITH date_series AS (
    SELECT 
        CAST(date_series AS DATE) AS date
    FROM 
        UNNEST(
            SEQUENCE(
                (SELECT MIN(date) FROM {{ ref('sp500_index_bronze') }}),
                (SELECT MAX(date) FROM {{ ref('sp500_index_bronze') }}),
                INTERVAL '1' DAY
            )
        ) AS t(date_series)
)

SELECT
    ds.date
FROM
    date_series ds
LEFT JOIN
    {{ ref('sp500_index_bronze') }} s
ON
    ds.date = s.date
WHERE
    s.date IS NULL;
