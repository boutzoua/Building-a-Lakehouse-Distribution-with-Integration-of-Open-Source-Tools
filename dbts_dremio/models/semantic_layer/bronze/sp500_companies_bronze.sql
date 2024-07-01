{{ config(materialized='view',schema="Data Analytics.bronze") }}

SELECT
    *
FROM {{ ref('src_sp500_companies') }}