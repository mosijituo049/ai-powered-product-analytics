from src.config import PROJECT_ID, DATASET_ID

def get_dataset_overview():
    return f"""
    SELECT
        COUNT(*) AS total_events,
        COUNT(DISTINCT user_pseudo_id) AS total_users,
        COUNT(DISTINCT ga_session_id) AS total_sessions,
        MIN(event_date) AS start_date,
        MAX(event_date) AS end_date
    FROM `{PROJECT_ID}.{DATASET_ID}.stg_events`
    """

def get_sessions():
    return f"""
    SELECT
        *
    FROM `{PROJECT_ID}.{DATASET_ID}.int_sessions`
    """

def get_event_distribution():
    return f"""
    SELECT
        event_name,
        COUNT(*) AS event_count
    FROM `{PROJECT_ID}.{DATASET_ID}.stg_events`
    GROUP BY event_name
    ORDER BY event_count DESC
    """

def get_device_distribution():
    return f"""
    SELECT
        device_category,
        COUNT(*) AS events
    FROM `{PROJECT_ID}.{DATASET_ID}.stg_events`
    GROUP BY device_category
    ORDER BY events DESC
    """

def get_source_distribution():
    return f"""
    SELECT
        acquisition_channel,
        COUNT(*) AS sessions
    FROM `{PROJECT_ID}.{DATASET_ID}.mart_purchase_prediction`
    GROUP BY acquisition_channel
    ORDER BY sessions DESC
    """

def get_country_distribution():
    return f"""
    SELECT
        country,
        COUNT(*) AS sessions
    FROM `{PROJECT_ID}.{DATASET_ID}.stg_events`
    GROUP BY country
    ORDER BY sessions DESC
    """

def get_session_summary():
    return f"""
    SELECT
        COUNT(*) AS total_sessions,
        AVG(session_duration_sec) AS avg_session_duration,
        AVG(total_events) AS avg_events,
        AVG(pageviews) AS avg_pageviews,
        AVG(item_views) AS avg_item_views
    FROM `{PROJECT_ID}.{DATASET_ID}.int_sessions`
    """

def get_purchase_distribution():
    return f"""
    SELECT
        purchased,
        COUNT(*) AS sessions
    FROM `{PROJECT_ID}.{DATASET_ID}.int_sessions`
    GROUP BY purchased
    ORDER BY purchased
    """

def get_checkout_abandonment_distribution():
    return f"""
    SELECT
        checkout_abandoned,
        COUNT(*) AS sessions
    FROM `{PROJECT_ID}.{DATASET_ID}.int_sessions`
    GROUP BY checkout_abandoned
    ORDER BY checkout_abandoned
    """

def get_session_duration():
    return f"""
    SELECT
        session_duration_sec
    FROM `{PROJECT_ID}.{DATASET_ID}.int_sessions`
    """

def get_total_events():
    return f"""
    SELECT
        total_events
    FROM `{PROJECT_ID}.{DATASET_ID}.int_sessions`
    """

def get_pageviews():
    return f"""
    SELECT
        pageviews
    FROM `{PROJECT_ID}.{DATASET_ID}.int_sessions`
    """

def get_missing_summary():
    return f"""
    SELECT
        COUNT(*) AS total_rows,

        COUNTIF(user_pseudo_id IS NULL) AS missing_user,

        COUNTIF(ga_session_id IS NULL) AS missing_session,

        COUNTIF(event_name IS NULL) AS missing_event

    FROM `{PROJECT_ID}.{DATASET_ID}.stg_events`
    """

def get_duplicate_summary():
    return f"""
    SELECT

        COUNT(*) AS total_rows,

        COUNT(DISTINCT ga_session_id) AS unique_sessions

    FROM `{PROJECT_ID}.{DATASET_ID}.int_sessions`
    """


def get_funnel_data():
    return f"""
    SELECT
        *
    FROM `{PROJECT_ID}.{DATASET_ID}.mart_funnel`
    ORDER BY sessions DESC
    """

def get_checkout_abandonment_data():
    return f"""
    SELECT
        *
    FROM `{PROJECT_ID}.{DATASET_ID}.mart_checkout_abandonment`
    """

def get_purchase_prediction_data():
    return f"""
    SELECT
        *
    FROM `{PROJECT_ID}.{DATASET_ID}.mart_purchase_prediction`
    """

def get_checkout_kpis():
    return f"""
    SELECT
        COUNT(*) AS checkout_sessions,

        COUNTIF(purchased = TRUE) AS purchase_sessions,

        COUNTIF(checkout_abandoned = TRUE) AS abandoned_sessions,

        AVG(session_duration_sec) AS avg_session_duration

    FROM `{PROJECT_ID}.{DATASET_ID}.int_sessions`
    WHERE begin_checkout > 0
    """

def get_checkout_funnel():
    return f"""
    SELECT
        COUNTIF(begin_checkout > 0) AS begin_checkout,
        COUNTIF(add_shipping_info > 0) AS add_shipping,
        COUNTIF(add_payment_info > 0) AS add_payment,
        COUNTIF(purchased = TRUE) AS purchase
    FROM `{PROJECT_ID}.{DATASET_ID}.int_sessions`
    """

def get_funnel_metrics():
    return f"""
        WITH funnel AS (
            SELECT
                stage,
                sessions,
                overall_conversion_rate
            FROM `{PROJECT_ID}.{DATASET_ID}.mart_funnel`
        ),

        funnel_with_previous AS (
            SELECT
                stage,
                sessions,
                overall_conversion_rate,
                LAG(sessions) OVER (
                    ORDER BY
                        CASE stage
                            WHEN 'Page View' THEN 1
                            WHEN 'View Item' THEN 2
                            WHEN 'Add to Cart' THEN 3
                            WHEN 'Begin Checkout' THEN 4
                            WHEN 'Purchase' THEN 5
                        END
                ) AS previous_sessions
            FROM funnel
        )

        SELECT
            stage,
            sessions,
            overall_conversion_rate,
            CASE
                WHEN previous_sessions IS NULL THEN 0
                WHEN previous_sessions = 0 THEN 0
                ELSE ROUND(
                    (1 - SAFE_DIVIDE(sessions, previous_sessions)) * 100,
                    2
                )
            END AS stage_dropoff_rate
        FROM funnel_with_previous

        ORDER BY
            CASE stage
                WHEN 'Page View' THEN 1
                WHEN 'View Item' THEN 2
                WHEN 'Add to Cart' THEN 3
                WHEN 'Begin Checkout' THEN 4
                WHEN 'Purchase' THEN 5
            END
    """


def get_abandonment_by_device():
    return f"""
    SELECT
        device_category,
        COUNT(*) AS checkout_sessions,
        COUNTIF(checkout_abandoned = TRUE) AS abandoned_sessions,
        ROUND(
            SAFE_DIVIDE(
                COUNTIF(checkout_abandoned = TRUE),
                COUNT(*)
            ) * 100,
            2
        ) AS abandonment_rate
    FROM `{PROJECT_ID}.{DATASET_ID}.int_sessions`
    WHERE begin_checkout > 0
    GROUP BY device_category
    ORDER BY abandonment_rate DESC
    """


def get_abandonment_by_channel():
    return f"""
    SELECT
        acquisition_channel,
        COUNT(*) AS checkout_sessions,
        COUNTIF(purchased = FALSE) AS abandoned_sessions,
        ROUND(
            SAFE_DIVIDE(
                COUNTIF(purchased = FALSE),
                COUNT(*)
            ) * 100,
            2
        ) AS abandonment_rate
    FROM `{PROJECT_ID}.{DATASET_ID}.mart_purchase_prediction`
    WHERE begin_checkout > 0
    GROUP BY acquisition_channel
    ORDER BY abandonment_rate DESC
    """