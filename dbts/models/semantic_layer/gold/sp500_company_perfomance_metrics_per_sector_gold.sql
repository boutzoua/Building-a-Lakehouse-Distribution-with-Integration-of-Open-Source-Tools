{{ config(materialized='view', schema="gold") }}

SELECT
    symbol,
    sector,
    AVG(marketcap) AS avg_marketcap,
    AVG(ebitda) AS avg_ebitda,
    AVG(revenuegrowth) AS avg_revenuegrowth,
    AVG(fulltimeemployees) AS avg_fulltimeemployees,
    AVG(weight) AS avg_weight
FROM {{ ref('sp500_companies_silver') }}
GROUP BY
    symbol, sector;
