{{
    config(
        materialized='incremental',
        unique_key='supplier_cuit',
        tags=["sourcePostgres"]
    )
}}

select * from {{source('staging', 'suppliers')}}