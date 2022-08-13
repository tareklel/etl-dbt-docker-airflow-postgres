{{
    config(
        materialized='incremental',
        unique_key='company_catalogue_id',
        tags=["sourcePostgres"]
    )
}}

select * from {{source('staging', 'company_catalogue')}}