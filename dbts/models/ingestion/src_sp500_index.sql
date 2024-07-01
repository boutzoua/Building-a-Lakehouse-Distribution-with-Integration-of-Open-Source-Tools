{{ config(materialized='incremental', unique_key='_id') }}

with source as (

    select
        *
    from {{ source('oltp', 'sp500_index') }}

)

select * from source

{% if is_incremental() %}

    -- this filter will only be applied on an incremental run
    where 'date' > (select max('date') from {{ this }})

{% endif %}