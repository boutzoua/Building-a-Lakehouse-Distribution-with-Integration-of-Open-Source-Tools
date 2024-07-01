with source as (

    select
        *
    from {{ source('oltp', 'sp500_index') }}

)

select * from source
