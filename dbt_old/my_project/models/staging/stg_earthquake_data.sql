{{ config(
    materialized='table',
    unique_key='id'
)}}

with source as (
select *
from {{ source('dev', 'raw_earthquake_data') }}
)

-- de_dup as (
--     select
--         *,
--         row_number() over (partition by id order by time desc) as rn
--     from source
-- )

select
    id,
    magnitude,
    location,
    time
from source