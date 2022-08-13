{{
    config(
        materialized='incremental',
        unique_key='company_order_id',
        tags=["sourcePostgres"]
    )
}}

select * from {{source('staging', 'company_order')}}