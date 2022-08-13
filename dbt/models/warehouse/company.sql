{{
    config(
        materialized='incremental',
        unique_key='company_cuit',
        tags=["sourcePostgres"]
    )
}}

select * from {{source('staging', 'company')}}