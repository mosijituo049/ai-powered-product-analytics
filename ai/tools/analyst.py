from src.database import query_to_dataframe

from src.services import (
    load_abandonment_by_channel,
    load_abandonment_by_device,
    load_checkout_kpis,
    load_funnel,
    load_funnel_metrics,
)
import joblib
import pandas as pd

from src.config import PROJECT_ID, DATASET_ID

def get_checkout_abandonment() -> dict:
    """
    Return checkout abandonment KPIs from the GA4 dataset.
    """

    df = load_checkout_kpis()

    if df.empty:
        raise ValueError("No checkout KPI data returned.")

    row = df.iloc[0]

    checkout_sessions = int(row["checkout_sessions"])
    purchase_sessions = int(row["purchase_sessions"])
    abandoned_sessions = int(row["abandoned_sessions"])

    abandonment_rate = (
        abandoned_sessions / checkout_sessions * 100
        if checkout_sessions > 0
        else 0
    )

    return {
        "checkout_sessions": checkout_sessions,
        "purchase_sessions": purchase_sessions,
        "abandoned_sessions": abandoned_sessions,
        "abandonment_rate": round(abandonment_rate, 2),
        "avg_session_duration": float(row["avg_session_duration"]),
    }

def get_funnel_metrics() -> dict:
    """
    Return calculated e-commerce funnel metrics
    and the largest stage drop-off.
    """
    df = load_funnel_metrics()

    if df.empty:
        raise ValueError("No funnel data returned.")

    records = df.to_dict(orient="records")

    largest_dropoff = max(
        records,
        key=lambda x: x["stage_dropoff_rate"],
    )

    return {
        "stages": records,
        "largest_dropoff": {
            "stage": largest_dropoff["stage"],
            "rate": largest_dropoff["stage_dropoff_rate"],
        },
    }

def get_abandonment_by_device() -> dict:
    df = load_abandonment_by_device()

    if df.empty:
        raise ValueError("No abandonment data returned.")

    records = df.to_dict(orient="records")

    highest = max(
        records,
        key=lambda x: x["abandonment_rate"],
    )

    return {
        "devices": records,
        "highest_abandonment_device": {
            "device_category": highest["device_category"],
            "abandonment_rate": highest["abandonment_rate"],
        },
    }


def get_abandonment_by_channel() -> list[dict]:
    """
    Return checkout abandonment metrics by acquisition channel.
    """
    df = load_abandonment_by_channel()

    if df.empty:
        raise ValueError("No abandonment data returned.")

    return df.to_dict(orient="records")


MODEL_PATH = "models/tuned_rf_model.pkl"


def get_purchase_prediction(session_id: int) -> dict:
    """
    Predict purchase probability for a specific checkout session.
    """

    query = f"""
        SELECT
            ga_session_id,
            session_duration_sec,
            total_events,
            total_engagement_time,
            pageviews,
            unique_pages,
            item_views,
            searches,
            add_to_cart,
            begin_checkout,
            device_category,
            operating_system,
            country,
            acquisition_channel
        FROM `{PROJECT_ID}.{DATASET_ID}.mart_checkout_abandonment`
        WHERE ga_session_id = {int(session_id)}
        LIMIT 1
    """

    df = query_to_dataframe(query)

    if df.empty:
        raise ValueError(
            f"Session ID {session_id} was not found "
            "in checkout abandonment data."
        )

    # Feature engineering
    df["engagement_per_event"] = (
        df["total_engagement_time"]
        / df["total_events"].replace(0, 1)
    )

    df["item_view_rate"] = (
        df["item_views"]
        / df["pageviews"].replace(0, 1)
    )

    df["checkout_ratio"] = (
        df["begin_checkout"]
        / df["add_to_cart"].replace(0, 1)
    )

    # Features used by the trained model
    model_features = [
        "session_duration_sec",
        "total_events",
        "total_engagement_time",
        "pageviews",
        "unique_pages",
        "item_views",
        "searches",
        "add_to_cart",
        "begin_checkout",
        "engagement_per_event",
        "item_view_rate",
        "checkout_ratio",
        "device_category",
        "operating_system",
        "country",
        "acquisition_channel",
    ]

    X = df[model_features]

    # Load trained pipeline
    model = joblib.load(MODEL_PATH)

    prediction = model.predict(X)[0]
    probability = model.predict_proba(X)[0][1]

    return {
        "session_id": int(session_id),

        "prediction": bool(prediction),

        "purchase_probability": round(
            float(probability),
            4
        ),

        "session_features": {
            # Session behaviour
            "session_duration_sec": float(
                df.iloc[0]["session_duration_sec"]
            ),
            "total_events": int(
                df.iloc[0]["total_events"]
            ),
            "total_engagement_time": float(
                df.iloc[0]["total_engagement_time"]
            ),
            "pageviews": int(
                df.iloc[0]["pageviews"]
            ),
            "unique_pages": int(
                df.iloc[0]["unique_pages"]
            ),
            "item_views": int(
                df.iloc[0]["item_views"]
            ),
            "searches": int(
                df.iloc[0]["searches"]
            ),
            "add_to_cart": int(
                df.iloc[0]["add_to_cart"]
            ),
            "begin_checkout": int(
                df.iloc[0]["begin_checkout"]
            ),

            # Derived behavioural features
            "engagement_per_event": float(
                df.iloc[0]["engagement_per_event"]
            ),
            "item_view_rate": float(
                df.iloc[0]["item_view_rate"]
            ),
            "checkout_ratio": float(
                df.iloc[0]["checkout_ratio"]
            ),

            # Context
            "device_category": df.iloc[0]["device_category"],
            "operating_system": df.iloc[0]["operating_system"],
            "country": df.iloc[0]["country"],
            "acquisition_channel": df.iloc[0]["acquisition_channel"],
        },
    }