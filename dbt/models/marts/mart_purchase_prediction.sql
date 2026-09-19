{{ config(
    materialized='table'
) }}

SELECT

    ------------------------------------------------------------------
    -- Session Metrics
    ------------------------------------------------------------------
    ga_session_id,
    
    session_duration_sec,

    total_events,

    total_engagement_time,

    ------------------------------------------------------------------
    -- Behaviour Features
    ------------------------------------------------------------------

    pageviews,

    unique_pages,

    item_views,

    searches,

    add_to_cart,

    begin_checkout,

    add_shipping_info,

    add_payment_info,

    ------------------------------------------------------------------
    -- Device
    ------------------------------------------------------------------

    device_category,

    operating_system,

    ------------------------------------------------------------------
    -- Geography
    ------------------------------------------------------------------

    country,

    ------------------------------------------------------------------
    -- Acquisition
    ------------------------------------------------------------------

    session_source,

    acquisition_channel,

    session_medium,

    session_campaign,

    ------------------------------------------------------------------
    -- Feature Engineering
    ------------------------------------------------------------------

    COALESCE(
        SAFE_DIVIDE(total_engagement_time, total_events),
        0
    ) AS engagement_per_event,

    COALESCE(
        SAFE_DIVIDE(item_views, pageviews),
        0
    ) AS item_view_rate,

    COALESCE(
        SAFE_DIVIDE(begin_checkout, add_to_cart),
        0
    ) AS checkout_ratio,

    ------------------------------------------------------------------
    -- Label
    ------------------------------------------------------------------

    purchased

FROM {{ ref('mart_checkout_abandonment') }}