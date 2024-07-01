{{ config(materialized='view', schema="Data Analytics.silver") }}

SELECT 
    Exchange,
    TRIM(UPPER(Symbol)) AS Symbol,
    TRIM(UPPER(Shortname)) AS Shortname,
    TRIM(UPPER(Industry)) AS Industry,
    Currentprice,
    Marketcap,
    Ebitda,
    Revenuegrowth,
    TRIM(UPPER(City)) AS City,
    TRIM(UPPER(State)) AS State,
    TRIM(UPPER(Country)) AS Country,
    Fulltimeemployees,
    Weight
FROM {{ ref('sp500_companies_silver') }}
WHERE Sector = 'Healthcare'