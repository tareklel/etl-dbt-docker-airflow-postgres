{{
    config(
        materialized='incremental',
        tags=["access_logs"]
    )
}}

select 
    a.*, 
    i.country 
from (select *, (regexp_match(useragent,'\(([^\(]+?)\;'))[1] as device from {{source('staging', 'access_logs')}}) as a 
inner join 
    {{source('dbt_dwh','ip_to_country')}} i 
on 
    cast(replace(a.ip_address,'.','') as bigint) 
between ip_address_start and ip_address_end