{{
    config(
        materialized='incremental',
        unique_key='customer_order_id',
        tags=["sourcePostgres"]
    )
}}

select * from {{source('staging', 'customer_order')}}