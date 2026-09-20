import streamlit as st
import plotly.express as px
import pandas as pd

from utils import load_css
from src.services import (
    load_checkout_abandonment,
    load_checkout_kpis,
    load_checkout_funnel
)

load_css()

st.title("🛒 Checkout Analysis")

with st.spinner("🛒 Loading checkout analytics..."):
    checkout_abandonment = load_checkout_abandonment()
    checkout_kpi = load_checkout_kpis()
    checkout_funnel = load_checkout_funnel()

st.divider()

#Checkout KPI
kpi = checkout_kpi.iloc[0]

with st.container():
    st.subheader("📊 Checkout Overview")
    col1, col2, col3, col4 = st.columns(4)
    
    col1.metric(
        label="Checkout Sessions",
        value=f"{kpi['checkout_sessions']:,}"
    )
    
    col2.metric(
        label="Purchase Sessions",
        value=f"{kpi['purchase_sessions']:,}"
    )

    abandonment_rate = (
        kpi["abandoned_sessions"] /
        kpi["checkout_sessions"]
    )
    col3.metric(
        label="Abandonment Rate",
        value=f"{abandonment_rate:.1%}"
    )

    col4.metric(
        label="Avg Session Duration",
        value=f"{kpi['avg_session_duration']:.0f} sec"
    )

    st.caption(
        """
    These KPIs provide an overview of checkout performance,
    including completed purchases, abandonment rate,
    and average session duration.
    """
    )


#Checkout Funnel -> Payment Funnel

funnel = checkout_funnel.iloc[0]

funnel_df = pd.DataFrame({
    "Stage": [
        "Begin Checkout",
        "Shipping",
        "Payment",
        "Purchase"
    ],
    "Users": [
        funnel["begin_checkout"],
        funnel["add_shipping"],
        funnel["add_payment"],
        funnel["purchase"]
    ]
})

funnel_df["Stage Conversion"] = (
    funnel_df["Users"] /
    funnel_df["Users"].shift(1)
)

funnel_df.loc[0, "Stage Conversion"] = 1

funnel_df["Overall Conversion"] = (
    funnel_df["Users"] /
    funnel_df["Users"].iloc[0]
)
funnel_df["Drop-off"] = (
    1 - funnel_df["Stage Conversion"]
)

st.divider()

with st.container():
    st.subheader("🛒 Checkout Funnel")

    fig = px.funnel(

        funnel_df,

        x="Users",

        y="Stage",

        title="Checkout Conversion Funnel"
    )

    fig.update_layout(

        height=500,

        title_x=0.5,

        margin=dict(
            l=20,
            r=20,
            t=60,
            b=20
        )
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )

    funnel_df["Conversion Rate"] = (
        funnel_df["Users"] /
        funnel_df["Users"].iloc[0]
    )

    st.dataframe(
        funnel_df,
        hide_index=True,
        width="stretch"
    )

#Checkout Abandonment Analysis
st.divider()

with st.container():
    st.subheader("🚪 Checkout Abandonment Analysis")

    st.markdown(
        """
    Compare completed and abandoned checkout sessions to identify
    potential friction points in the purchase journey.
    """
    )

    left_col, right_col = st.columns(2)
    with left_col:
        st.markdown("#### Checkout Session Distribution")
        abandonment_summary = (
            checkout_abandonment
            .groupby("checkout_abandoned")
            .size()
            .reset_index(name="Sessions")
        )

        abandonment_summary["Status"] = abandonment_summary[
            "checkout_abandoned"
        ].map({
            False: "Completed",
            True: "Abandoned"
        })

        fig = px.pie(
            abandonment_summary,
            names="Status",
            values="Sessions",
            hole=0.45,
            title="Checkout Session Distribution"
        )

        st.plotly_chart(
            fig,
            width="stretch"
        )
    
    with right_col:
        st.markdown("#### Behaviour Comparison")
        behaviour = (
            checkout_abandonment
            .groupby("checkout_abandoned")
            .agg(
                Avg_Duration=("session_duration_sec","mean"),
                Avg_Pageviews=("pageviews","mean"),
                Avg_ItemViews=("item_views","mean")
            )
            .round(1)
        )

        fig = px.bar(
            behaviour.reset_index(),
            x="checkout_abandoned",
            y="Avg_Duration",
            color="checkout_abandoned",
            title="Average Session Duration"
        )

        st.plotly_chart(
            fig,
            width="stretch"
        )

    st.markdown("#### Key Findings")
    st.info("""
    • Completed sessions generally exhibit stronger engagement.

    • Abandoned sessions tend to have fewer interactions before exiting.

    • Optimising the checkout flow may reduce abandonment.
    """)

#Abandonment -> Device

st.divider()
with st.container():
    st.subheader("📱 Segment Analysis")

    st.markdown("""
    Compare checkout performance across different user segments
    to identify opportunities for optimisation.
    """)

    tab1, tab2, tab3 = st.tabs(
        [
            "📱 Device",
            "🌍 Country",
            "📈 Traffic Source"
        ]
    )

    with tab1:
        st.markdown("#### Purchase Rate by Device")
        device_summary = (
            checkout_abandonment
            .groupby("device_category")
            .agg(
                Sessions=("purchased","count"),
                Purchase_Rate=("purchased","mean")
            )
            .round(3)
            .reset_index()
        )
        fig = px.bar(
            device_summary,
            x="device_category",
            y="Purchase_Rate",
            color="device_category",
            text="Purchase_Rate",
            title="Purchase Rate by Device"
        )

        fig.update_traces(
            texttemplate="%{text:.1%}"
        )

        st.plotly_chart(
            fig,
            width="stretch"
        )
        st.dataframe(
            device_summary,
            hide_index=True,
            width="stretch"
        )

    with tab2:
        st.markdown("#### Purchase Rate by Country")
        country_summary = (
            checkout_abandonment
            .groupby("country")
            .agg(
                Sessions=("purchased","count"),
                Purchase_Rate=("purchased","mean")
            )
            .query("Sessions >= 50")
            .round(3)
            .reset_index()
        )

        fig = px.bar(
            country_summary,
            x="country",
            y="Purchase_Rate",
            color="Purchase_Rate",
            color_continuous_scale="Blues",
            text="Purchase_Rate"
        )

        fig.update_traces(
            texttemplate="%{text:.1%}"
        )

        st.plotly_chart(
            fig,
            width="stretch"
        )

    with tab3:
        st.markdown("#### Purchase Rate by Traffic Source")
        source_summary = (
            checkout_abandonment
            .groupby("acquisition_channel")
            .agg(
                Sessions=("purchased","count"),
                Purchase_Rate=("purchased","mean")
            )
            .query("Sessions >= 20")
            .round(3)
            .reset_index()
        )

        fig = px.bar(
            source_summary,
            x="acquisition_channel",
            y="Purchase_Rate",
            color="Purchase_Rate",
            color_continuous_scale="Viridis",
            text="Purchase_Rate"
        )

        fig.update_traces(
            texttemplate="%{text:.1%}"
        )

        st.plotly_chart(
            fig,
            width="stretch"
        )

#Insights
st.divider()
st.subheader("💡 Business Insights")

st.success("""
### Key Takeaways

- Identify the checkout stage with the highest drop-off rate.
- Compare purchase performance across device types.
- Evaluate which traffic sources drive higher-quality sessions.
- Use these insights to prioritise checkout optimisation and marketing efforts.
""")
