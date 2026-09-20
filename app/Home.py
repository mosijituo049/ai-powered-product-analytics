import pandas as pd

import streamlit as st
import plotly.express as px

from utils import load_css
from src.services import load_home_data


# =========================
# Page configuration
# =========================

st.set_page_config(
    page_title="GA4 Product Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

load_css()


# =========================
# Header
# =========================

st.title("📊 GA4 Product Analytics Platform")

st.markdown("""
### Business Question

**What drives checkout abandonment, and how can we identify high-intent users before they leave?**

This dashboard analyses user behaviour across the purchase funnel,
identifies key conversion bottlenecks, and applies machine learning
to predict purchase intent.
""")

st.caption(
    """
    Monitor user behaviour, identify conversion bottlenecks,
    and predict purchase intent.
    """
)

st.divider()


# =========================
# Load data
# =========================

with st.spinner("📊 Loading analytics data..."):
    home = load_home_data()


# =========================
# Prepare data
# =========================

overview_data = home[home["section"] == "overview"]

funnel = home[home["section"] == "funnel"].copy()

device = home[home["section"] == "device"].copy()

country = home[home["section"] == "country"].copy()

source = home[home["section"] == "source"].copy()


overview = {
    row["dimension"]: row["value"]
    for _, row in overview_data.iterrows()
}


funnel = funnel.rename(
    columns={
        "dimension": "stage",
        "value": "sessions",
        "rate": "overall_conversion_rate"
    }
)

device = device.rename(
    columns={
        "dimension": "device_category",
        "value": "events"
    }
)

country = country.rename(
    columns={
        "dimension": "country",
        "value": "sessions"
    }
)

source = source.rename(
    columns={
        "dimension": "acquisition_channel",
        "value": "sessions"
    }
)


purchase = funnel.loc[
    funnel["stage"] == "Purchase",
    "sessions"
].iloc[0]

conversion = funnel.loc[
    funnel["stage"] == "Purchase",
    "overall_conversion_rate"
].iloc[0]


# =========================
# Executive Summary
# =========================

with st.container():
    st.subheader("Executive Summary")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Users", f"{int(overview['total_users']):,}")

    with col2:
        st.metric("Sessions", f"{int(overview['total_sessions']):,}")

    with col3:
        st.metric("Purchases", f"{int(purchase):,}")

    with col4:
        st.metric("Conversion", f"{conversion:.2f}%")

st.divider()

st.subheader("🧭 Dashboard Guide")

st.info("""
**Dashboard Structure**

📈 Funnel Analysis

→ Understand where users leave the purchase journey.

🛒 Checkout Analysis

→ Identify checkout abandonment patterns and compare user segments.

🤖 Purchase Prediction

→ Predict purchase intent using a Random Forest model.
""")

st.divider()

#Overview
with st.container():
    st.subheader("📊 Dataset Overview")

    col5,col6 = st.columns(2)

    with col5:
        funnel_order = [
            "Page View",
            "View Item",
            "Add to Cart",
            "Begin Checkout",
            "Purchase"
        ]

        funnel["stage"] = pd.Categorical(
            funnel["stage"],
            categories=funnel_order,
            ordered=True
        )

        funnel = funnel.sort_values("stage")

        fig_funnel = px.funnel(
            funnel,
            y="stage",
            x="sessions"
        )

        st.plotly_chart(
            fig_funnel,
            width="stretch"
        )

    with col6:
        fig_device = px.pie(
            device,
            names="device_category",
            values="events",
            hole=0.5
        )

        st.plotly_chart(
            fig_device,
            width="stretch"
        )

    col7,col8 = st.columns(2)

    with col7:
        source_top = source.head(10)

        source_top = source_top.sort_values("sessions", ascending=True)

        fig_traffic = px.bar(
            source_top,
            x="sessions",
            y="acquisition_channel",
            orientation="h",
            text="sessions"
        )

        st.plotly_chart(fig_traffic, width="stretch")

    with col8:
        country_top = (
            country
            .sort_values("sessions", ascending=False)
            .head(10)
        )

        fig_country = px.bar(
            country_top,
            x="sessions",
            y="country",
            orientation="h",
            text="sessions"
        )

        fig_country.update_layout(
            yaxis={"categoryorder": "total ascending"},
            height=450
        )

        st.plotly_chart(fig_country, width="stretch")

st.divider()

#Quick Insights
with st.container():
    st.subheader("💡 Quick Insights")
    st.info(
    """
    • Largest drop-off occurs between View Item and Add to Cart.

    • Mobile generates the majority of traffic.

    • Purchase conversion remains below 5%.

    • Funnel optimization should focus on Product Detail Pages.
    """
    )

if __name__ == "__main__":
    print("Home Page")