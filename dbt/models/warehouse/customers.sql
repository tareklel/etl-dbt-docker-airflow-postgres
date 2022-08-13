{{
    config(
        materialized='incremental',
        unique_key='doc_number',
        tags=["sourcePostgres"]
    )
}}

select * from {{source('staging', 'customers')}}