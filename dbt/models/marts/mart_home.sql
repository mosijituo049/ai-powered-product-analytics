{{ config(
    materialized='table'
) }}

WITH overview AS (

    SELECT
        'overview' AS section,
        'total_events' AS dimension,
        COUNT(*) AS value,
        CAST(NULL AS FLOAT64) AS rate,
        MIN(event_date) AS start_date,
        MAX(event_date) AS end_date
    FROM {{ ref('stg_events') }}

    UNION ALL

    SELECT
        'overview',
        'total_users',
        COUNT(DISTINCT user_pseudo_id),
        NULL,
        NULL,
        NULL
    FROM {{ ref('stg_events') }}

    UNION ALL

    SELECT
        'overview',
        'total_sessions',
        COUNT(DISTINCT ga_session_id),
        NULL,
        NULL,
        NULL
    FROM {{ ref('stg_events') }}

),

device AS (

    SELECT
        'device' AS section,
        device_category AS dimension,
        COUNT(*) AS value,
        CAST(NULL AS FLOAT64) AS rate,
        CAST(NULL AS DATE) AS start_date,
        CAST(NULL AS DATE) AS end_date
    FROM {{ ref('stg_events') }}
    GROUP BY device_category

),

country AS (

    SELECT
        'country' AS section,
        country AS dimension,
        COUNT(*) AS value,
        CAST(NULL AS FLOAT64) AS rate,
        CAST(NULL AS DATE) AS start_date,
        CAST(NULL AS DATE) AS end_date
    FROM {{ ref('int_sessions') }}
    GROUP BY country

),

source AS (

    SELECT
        'source' AS section,
        acquisition_channel AS dimension,
        COUNT(*) AS value,
        CAST(NULL AS FLOAT64) AS rate,
        CAST(NULL AS DATE) AS start_date,
        CAST(NULL AS DATE) AS end_date
    FROM {{ ref('mart_purchase_prediction') }}
    GROUP BY acquisition_channel

),

funnel AS (

    SELECT
        'funnel' AS section,
        stage AS dimension,
        sessions AS value,
        overall_conversion_rate AS rate,
        CAST(NULL AS DATE) AS start_date,
        CAST(NULL AS DATE) AS end_date
    FROM {{ ref('mart_funnel') }}

)

SELECT * FROM overview
UNION ALL
SELECT * FROM device
UNION ALL
SELECT * FROM country
UNION ALL
SELECT * FROM source
UNION ALL
SELECT * FROM funnel