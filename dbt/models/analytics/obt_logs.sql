{{ config(
    tags=["access_logs"]
) }}

select 
    country,
    device,
    sum(1) as total_visits
from 
    {{ref('log')}} o 
group by 1,2
order by total_visits desc