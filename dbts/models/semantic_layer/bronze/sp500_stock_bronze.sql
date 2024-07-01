{{ config(materialized='view',schema="bronze") }}

SELECT
    *
FROM {{ ref('src_sp500_stock') }}