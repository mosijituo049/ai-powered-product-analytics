from src.database import query_to_dataframe
import src.queries as queries
import streamlit as st

# ============================================================
# Data Understanding
# ============================================================

@st.cache_data(ttl=3600, show_spinner=False)
def load_home_data():
    return query_to_dataframe(queries.get_home_data())

@st.cache_data(ttl=600,show_spinner=False)
def load_event_distribution():

    return query_to_dataframe(
        queries.get_event_distribution()
    )

def load_sessions():

    return query_to_dataframe(
        queries.get_sessions()
    )

@st.cache_data(ttl=600,show_spinner=False)
def load_session_summary():

    return query_to_dataframe(
        queries.get_session_summary()
    )

@st.cache_data(ttl=600,show_spinner=False)
def load_purchase_distribution():
    """Load purchase distribution."""
    return query_to_dataframe(
        queries.get_purchase_distribution()
    )

@st.cache_data(ttl=600,show_spinner=False)
def load_checkout_distribution():
    """Load checkout abandonment distribution."""
    return query_to_dataframe(
        queries.get_checkout_abandonment_distribution()
    )

@st.cache_data(ttl=600,show_spinner=False)
def load_checkout_kpis():
    return query_to_dataframe(
        queries.get_checkout_kpis()
    )

@st.cache_data(ttl=600,show_spinner=False)
def load_checkout_funnel():
    return query_to_dataframe(
        queries.get_checkout_funnel()
    )

@st.cache_data(ttl=600,show_spinner=False)
def load_session_duration():
    """Load session duration."""
    return query_to_dataframe(
        queries.get_session_duration()
    )

@st.cache_data(ttl=600,show_spinner=False)
def load_total_events():
    """Load total events per session."""
    return query_to_dataframe(
        queries.get_total_events()
    )

@st.cache_data(ttl=600,show_spinner=False)
def load_pageviews():
    """Load pageviews per session."""
    return query_to_dataframe(
        queries.get_pageviews()
    )

@st.cache_data(ttl=600,show_spinner=False)
def load_missing_summary():
    """Load missing value summary."""
    return query_to_dataframe(
        queries.get_missing_summary()
    )

@st.cache_data(ttl=600,show_spinner=False)
def load_duplicate_summary():
    """Load duplicate session summary."""
    return query_to_dataframe(
        queries.get_duplicate_summary()
    )

@st.cache_data(ttl=600,show_spinner=False)
def load_funnel():
    return query_to_dataframe(
        queries.get_funnel_data()
    )

@st.cache_data(ttl=600,show_spinner=False)
def load_funnel_metrics():
    return query_to_dataframe(queries.get_funnel_metrics())

@st.cache_data(ttl=600,show_spinner=False)
def load_checkout_abandonment():
    return query_to_dataframe(
        queries.get_checkout_abandonment_data()
    )

@st.cache_data(ttl=600,show_spinner=False)
def load_purchase_prediction():
    return query_to_dataframe(
        queries.get_purchase_prediction_data()
    )

@st.cache_data(ttl=600, show_spinner=False)
def load_abandonment_by_device():
    return query_to_dataframe(
        queries.get_abandonment_by_device()
    )


@st.cache_data(ttl=600, show_spinner=False)
def load_abandonment_by_channel():
    return query_to_dataframe(
        queries.get_abandonment_by_channel()
    )