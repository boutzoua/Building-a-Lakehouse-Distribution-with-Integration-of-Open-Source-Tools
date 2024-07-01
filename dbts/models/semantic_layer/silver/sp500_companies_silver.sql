{{ config(materialized='view', schema="silver") }}

WITH column_averages AS (
    SELECT
        AVG(currentprice) AS avg_currentprice,
        AVG(marketcap) AS avg_marketcap,
        AVG(ebitda) AS avg_ebitda,
        AVG(revenuegrowth) AS avg_revenuegrowth,
        AVG(fulltimeemployees) AS avg_fulltimeemployees,
        AVG(weight) AS avg_weight
    FROM {{ ref('sp500_companies_bronze') }}
)

SELECT 
    bc.exchange,
    bc.symbol,
    bc.shortname,
    bc.sector,
    bc.industry,
    COALESCE(bc.currentprice, ca.avg_currentprice) AS currentprice,
    COALESCE(bc.marketcap, ca.avg_marketcap) AS marketcap,
    COALESCE(bc.ebitda, ca.avg_ebitda) AS ebitda,
    COALESCE(bc.revenuegrowth, ca.avg_revenuegrowth) AS revenuegrowth,
    bc.city,
    bc.state,
    bc.country,
    COALESCE(bc.fulltimeemployees, ca.avg_fulltimeemployees) AS fulltimeemployees,
    COALESCE(bc.weight, ca.avg_weight) AS weight
FROM {{ ref('sp500_companies_bronze') }} as bc, column_averages as ca;
