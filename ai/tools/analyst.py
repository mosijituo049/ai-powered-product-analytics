from src.services import load_checkout_kpis, load_funnel


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

def get_funnel_metrics() -> list[dict]:
    """
    Return e-commerce funnel metrics from the GA4 dataset.
    """

    df = load_funnel()

    if df.empty:
        raise ValueError("No funnel data returned.")

    return df.to_dict(orient="records")