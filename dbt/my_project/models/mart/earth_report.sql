{{ config(
    materialized='table',
    unique_key='dev'
) }}

with staging as (
    select * from {{ ref('stg_earthquake_data') }}
)

select
    *,
    -- Categorize intensity for map coloring
    case 
        when magnitude < 3.0 then '0-3 Minor'
        when magnitude >= 3.0 and magnitude < 5.0 then '3-5 Light'
        when magnitude >= 5.0 and magnitude < 7.0 then '5-7 Strong'
        else '7+ Major'
    end as magnitude_category,
    
    -- Create a simplified date for time-series charts
    date_trunc('day', occurred_at) as event_date
from staging