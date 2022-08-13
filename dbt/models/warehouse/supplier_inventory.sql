{{
    config(
        materialized='incremental',
        unique_key='supplier_inventory_id',
        tags=["sourcePostgres"]
    )
}}

select * from {{source('staging', 'supplier_inventory')}}