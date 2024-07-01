{{ config(materialized='view', schema="Data Analytics.gold") }}


SELECT Sector, SUM(Marketcap) AS Total_Marketcap,
       SUM(Marketcap) * 100.0 / (SELECT SUM(Marketcap) FROM {{ ref('sp500_companies_silver') }}) AS Marketcap_Percentage
FROM {{ ref('sp500_companies_silver') }}
GROUP BY Sector;