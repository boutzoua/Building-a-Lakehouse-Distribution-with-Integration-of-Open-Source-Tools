{{ config(materialized='incremental', unique_key='_id') }}

with source as (
    select
        *
    from {{ source('oltp', 'sp500_stock') }}
)

select * from source

{% if is_incremental() %}
    where 'date' > (select max('date') from {{ this }})
{% endif %}