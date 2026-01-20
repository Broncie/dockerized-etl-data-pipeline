{{ config(
    materialized='table',
    unique_key='dev'
) }}

select *
from {{ ref('stg_earthquake_data') }}