{{
    config(
        materialized='incremental',
        unique_key='product_id',
        tags=["sourcePostgres"]
    )
}}

select * from {{source('staging', 'products')}}