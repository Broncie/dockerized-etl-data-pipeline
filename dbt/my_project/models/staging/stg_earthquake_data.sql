{{ config(
    materialized='table',
    unique_key='id'
)}}

with source as (
    select *
    from {{ source('dev', 'raw_earthquake_data') }}
),

cleansed as (
    select
        id,
        -- The Python script lands this as TEXT; we cast to TIMESTAMP for analysis
        cast(time as timestamp) as occurred_at,
        
        -- Coordinates are already FLOAT from Python, but casting here 
        -- ensures dbt creates the correct column types in the new table
        cast(latitude as float) as latitude,
        cast(longitude as float) as longitude,
        cast(depth as float) as depth,
        
        -- Matching the Python column name 'magnitude'
        cast(magnitude as float) as magnitude,
        
        -- Renaming 'location' from Python to something more descriptive
        location as location_description
        
    from source
    -- Map Safety: ensure we have coordinates
    where latitude is not null 
      and longitude is not null
)

select * from cleansed