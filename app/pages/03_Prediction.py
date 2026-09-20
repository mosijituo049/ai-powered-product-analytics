import joblib
import pandas as pd
import streamlit as st
import plotly.express as px
from pathlib import Path

from utils import load_css
from src.services import (
    load_purchase_prediction
)

from ai.tool_calling import run_agent
from ai.tools.schemas import TOOL_SCHEMAS

tools = list(TOOL_SCHEMAS.values())

prediction_df = load_purchase_prediction()

BASE_DIR = Path(__file__).resolve().parents[2]

MODEL_PATH = BASE_DIR / "models" / "tuned_rf_model.pkl"

model = joblib.load(MODEL_PATH)

OUTPUT_DIR = BASE_DIR / "outputs"

comparison_df = pd.read_csv(
    OUTPUT_DIR / "model_comparison.csv"
)
comparison_df = comparison_df.round(3)

feature_df = pd.read_csv(
    OUTPUT_DIR / "feature_importance.csv"
)

load_css()

st.title("🤖 Purchase Intent Prediction")
st.markdown(
    """
Predict the probability that a user will complete a purchase based on
their session behaviour.
"""
)

st.divider()

best_model = comparison_df.loc[
    comparison_df["ROC-AUC"].idxmax()
]

with st.container():
    st.subheader("📊 Model Performance")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Accuracy",
        f"{best_model['Accuracy']:.3f}"
    )

    col2.metric(
        "Precision",
        f"{best_model['Precision']:.3f}"
    )

    col3.metric(
        "Recall",
        f"{best_model['Recall']:.3f}"
    )

    col4.metric(
        "ROC-AUC",
        f"{best_model['ROC-AUC']:.3f}"
    )

    st.success(
        f"🏆 Best Model: {best_model['Model']}"
    )

st.divider()

with st.container():
    st.subheader("📋 Model Comparison")

    st.dataframe(
        comparison_df,
        width="stretch",
        hide_index=True
    )

st.divider()

top_features = (
    feature_df
    .sort_values("Importance", ascending=False)
    .head(15)
)

with st.container():

    st.subheader("📈 Feature Importance")

    fig = px.bar(

        top_features.sort_values("Importance"),

        x="Importance",

        y="Feature",

        orientation="h",

        color="Importance",

        color_continuous_scale="Blues",

        text="Importance"
    )

    fig.update_traces(
        texttemplate="%{text:.3f}",
        textposition="outside"
    )

    fig.update_layout(

        xaxis_title="Importance Score",

        yaxis_title="",

        height=600,

        showlegend=False,

        margin=dict(
            l=10,
            r=10,
            t=20,
            b=20
        )
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )

    st.info(
        """
        Feature importance shows which behavioural and session-level features
        contribute most to the prediction model.

        Features with higher importance have a greater influence on estimating
        a user's purchase intent.
    """
    )

st.divider()

with st.container():
    st.subheader("📈 High Intent Distribution")

    st.markdown("""
    Predicted purchase intent across all sessions in the dataset.
    """)

    probability = model.predict_proba(prediction_df)[:, 1]
    prediction_df["purchase_probability"] = probability
    prediction_df["intent"] = pd.cut(
        prediction_df["purchase_probability"],
        bins=[0, 0.5, 0.8, 1],
        labels=[
            "Low",
            "Medium",
            "High"
        ]
    )

    intent_summary = (
        prediction_df["intent"]
        .value_counts()
        .rename_axis("Intent")
        .reset_index(name="Sessions")
    )

    intent_summary["Percentage"] = (
        intent_summary["Sessions"]
        / intent_summary["Sessions"].sum()
    )

    fig = px.bar(
        intent_summary,
        x="Intent",
        y="Percentage",
        color="Intent",
        text=intent_summary["Percentage"].map("{:.1%}".format)
    )

    fig.update_traces(
        textposition="outside"
    )

    fig.update_layout(
        showlegend=False
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )

st.divider()


with st.container():
    st.subheader("🎯 Predict Purchase Intent")

    st.markdown(
        "Search for a session and let the AI agent analyse its purchase intent."
    )

    # Get available session IDs
    session_ids = (
        prediction_df["ga_session_id"]
        .dropna()
        .astype(int)
        .unique()
        .tolist()
    )

    # Search
    search_term = st.text_input(
        "Search Session ID",
        placeholder="Enter part of a Session ID..."
    )

    selected_session_id = None

    if search_term:

        filtered_ids = [
            session_id
            for session_id in session_ids
            if search_term in str(session_id)
        ]

        if filtered_ids:

            filtered_ids = filtered_ids[:20]

            selected_session_id = st.selectbox(
                "Matching Sessions",
                filtered_ids
            )

        else:
            st.warning("No matching sessions found.")

    # Analyze
    if selected_session_id is not None:

        if st.button(
            "🚀 Analyze Session",
            width="stretch"
        ):

            question = f"""
                The user selected session ID {selected_session_id}.

                Analyze the purchase intent of this session.

                You MUST use the get_purchase_prediction tool
                with session_id={selected_session_id}.

                After receiving the tool result, provide a concise business-oriented analysis with these sections:

                1. Purchase Intent
                - Explain the purchase probability and prediction.

                2. Key Insight
                - Identify the most important behavioural signals from the session.
                - Explain why they may be relevant.
                - Base all observations strictly on the tool result.
                - Do not invent benchmarks, averages, or comparisons.

                3. Recommended Action
                - Suggest one or two practical product or business actions based on the observed behaviour.
                - Clearly distinguish recommendations from observed facts.

                Important data interpretation rules:
                - Use only the data returned by the tool.
                - Do not invent information, benchmarks, averages, or comparisons.
                - Do not interpret a ratio as a percentage unless it is explicitly defined as a percentage.
                - checkout_ratio = begin_checkout / add_to_cart.
                - checkout_ratio is a behavioural ratio, not a percentage and not a measure of time.
                - engagement_per_event = total_engagement_time / total_events.
                - Do not infer or convert the unit of total_engagement_time unless the unit is explicitly provided.
                - Do not describe a feature as "high" or "low" unless there is a valid reference point in the available data.
                - Keep the analysis concise and actionable.
                - Do not present hypotheses about technical issues or user motivations as established facts. Frame them as hypotheses or areas for investigation.
                """

            with st.spinner("🤖 AI is analysing the session..."):
                response, tool_results = run_agent(
                    question=question,
                    tools=tools
                )

            #st.write("DEBUG tool_results:")
            #st.write(tool_results)

            # Get structured tool result
            prediction_result = None

            for item in tool_results:
                if item["tool_name"] == "get_purchase_prediction":
                    prediction_result = item["result"]
                    break

            if prediction_result:
                probability = prediction_result["purchase_probability"]
                prediction = prediction_result["prediction"]
                features = prediction_result["session_features"]

                # Calculate intent level
                if probability >= 0.70:
                    intent_level = "High"
                elif probability >= 0.40:
                    intent_level = "Medium"
                else:
                    intent_level = "Low"

                st.subheader("📊 Purchase Intent")

                col1, col2, col3 = st.columns(3)

                with col1:
                    st.metric(
                        "Purchase Probability",
                        f"{probability:.2%}"
                    )

                with col2:
                    st.metric(
                        "Prediction",
                        "Purchase" if prediction else "No Purchase"
                    )

                with col3:
                    st.metric(
                        "Intent Level",
                        intent_level
                    )

                st.subheader("👤 Session Characteristics")

                characteristics = pd.DataFrame(
                    [
                        {
                            "Category": "Session Behaviour",
                            "Feature": "Session Duration (sec)",
                            "Value": str(features["session_duration_sec"]),
                        },
                        {
                            "Category": "Session Behaviour",
                            "Feature": "Total Events",
                            "Value": str(features["total_events"]),
                        },
                        {
                            "Category": "Session Behaviour",
                            "Feature": "Total Engagement Time",
                            "Value": str(features["total_engagement_time"]),
                        },
                        {
                            "Category": "Session Behaviour",
                            "Feature": "Pageviews",
                            "Value": str(features["pageviews"]),
                        },
                        {
                            "Category": "Session Behaviour",
                            "Feature": "Unique Pages",
                            "Value": str(features["unique_pages"]),
                        },
                        {
                            "Category": "Session Behaviour",
                            "Feature": "Item Views",
                            "Value": str(features["item_views"]),
                        },
                        {
                            "Category": "Session Behaviour",
                            "Feature": "Searches",
                            "Value": str(features["searches"]),
                        },
                        {
                            "Category": "Session Behaviour",
                            "Feature": "Add to Cart",
                            "Value": str(features["add_to_cart"]),
                        },
                        {
                            "Category": "Session Behaviour",
                            "Feature": "Begin Checkout",
                            "Value": str(features["begin_checkout"]),
                        },
                        {
                            "Category": "Derived Features",
                            "Feature": "Engagement per Event",
                            "Value": str(
                                round(features["engagement_per_event"], 3)
                            ),
                        },
                        {
                            "Category": "Derived Features",
                            "Feature": "Item View Rate",
                            "Value": str(
                                round(features["item_view_rate"], 3)
                            ),
                        },
                        {
                            "Category": "Derived Features",
                            "Feature": "Checkout Ratio",
                            "Value": str(
                                round(features["checkout_ratio"], 3)
                            ),
                        },
                        {
                            "Category": "Context",
                            "Feature": "Device",
                            "Value": str(features["device_category"]),
                        },
                        {
                            "Category": "Context",
                            "Feature": "Operating System",
                            "Value": str(features["operating_system"]),
                        },
                        {
                            "Category": "Context",
                            "Feature": "Country",
                            "Value": str(features["country"]),
                        },
                        {
                            "Category": "Context",
                            "Feature": "Acquisition Channel",
                            "Value": str(features["acquisition_channel"]),
                        },
                    ]
                )

                st.dataframe(
                    characteristics,
                    width="stretch",
                    hide_index=True,
                )

            st.subheader("🤖 AI Analysis")
            st.write(response.text)