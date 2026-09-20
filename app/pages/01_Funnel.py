import streamlit as st
import plotly.express as px

from utils import load_css
from src.services import (
    load_funnel
)

load_css()

funnel = load_funnel()

st.title("📈 Funnel Analysis")

st.divider()

#Funnel KPI
with st.container():
    st.subheader("📊 Funnel Overview")
    total_sessions = funnel["sessions"].iloc[0]

    overall_conversion = funnel["overall_conversion_rate"].iloc[-1]

    max_dropoff = funnel["stage_dropoff_rate"].max()

    purchase_sessions = funnel["sessions"].iloc[-1]

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Sessions",
        f"{total_sessions:,}"
    )

    col2.metric(
        "Overall Conversion",
        f"{overall_conversion:.2f}%"
    )

    col3.metric(
        "Max Drop-off",
        f"{max_dropoff:.2f}%"
    )

    col4.metric(
        "Purchases",
        f"{purchase_sessions:,}"
    )

    worst_stage = funnel.loc[
        funnel["stage_dropoff_rate"].idxmax(),
        "stage"
    ]

    st.caption(
        f"Highest drop-off occurs at **{worst_stage}**."
    )

st.divider()

#Overview
with st.container():
    st.subheader("📉 Funnel Performance")

    st.markdown(
        """
        Visualise the user journey from page view to purchase
        and identify the stages with the highest conversion loss.
        """
    )

    col1, col2 = st.columns(2)

    with col1:

        fig_funnel = px.funnel(
            funnel,
            y="stage",
            x="sessions",
            text="sessions",
            title="Overall Funnel"
        )

        fig_funnel.update_layout(
            height=500
        )

        st.plotly_chart(
            fig_funnel,
            width="stretch"
        )
    
    with col2:
        fig_dropoff = px.bar(
            funnel,
            x="stage",
            y="stage_dropoff_rate",
            color="stage_dropoff_rate",
            color_continuous_scale="Reds",
            text="stage_dropoff_rate",
            title="Drop-off Rate by Stage"
        )

        fig_dropoff.update_traces(
            texttemplate="%{text:.2f}%",
            textposition="outside"
        )

        fig_dropoff.update_layout(
            yaxis_title="Drop-off Rate (%)",
            xaxis_title="",
            coloraxis_showscale=False,
            height=500
        )

        st.plotly_chart(
            fig_dropoff,
            width="stretch"
        )
        
    st.dataframe(
        funnel,
        hide_index=True,
        width="stretch"
    )


st.divider()

#Key Insights
with st.container():
    st.subheader("💡 Key Insights")

    st.info("""
    ### Key Findings

    • The largest drop-off occurs between **View Item** and **Add to Cart** (80.17%).

    • Users who begin the checkout process are much more likely to continue, with a relatively high stage conversion rate.

    • Improving product engagement before checkout is likely to generate a greater impact than optimising the checkout flow alone.
    """)

st.divider()

#Recommendation
with st.container():
    st.subheader("Recommendation")

    st.success("""
    ### Suggested Actions

    - Improve product page content to encourage more Add-to-Cart actions.
    - Optimise product recommendations and merchandising.
    - Reduce friction before users reach the checkout stage.
    - Prioritise high-intent users for remarketing campaigns.
    """)