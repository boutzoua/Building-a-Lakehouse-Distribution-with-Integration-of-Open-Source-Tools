
with source as (
    select
        *
    from {{ source('oltp', 'sp500_stock') }}
)

select * from source
