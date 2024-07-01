with source as (
    select
        *
    from {{ source('oltp', 'sp500_companies') }}
)

select
    *
from source
