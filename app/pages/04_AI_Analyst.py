import streamlit as st

from utils import load_css
from ai.tool_calling import run_agent
from ai.tools.schemas import TOOL_SCHEMAS


# =========================
# Configuration
# =========================

tools = list(TOOL_SCHEMAS.values())

load_css()


# =========================
# Page Header
# =========================

st.title("🤖 AI Analyst")

st.markdown(
    """
Ask questions about your GA4 product analytics data.
The AI Analyst can use the available analytics tools to retrieve
data and provide business-oriented insights.
"""
)

st.divider()


# =========================
# Session State
# =========================

if "ai_messages" not in st.session_state:
    st.session_state.ai_messages = []


# =========================
# Example Questions
# =========================

st.subheader("💡 Example Questions")

example_questions = [
    "Why are users abandoning checkout?",
    "What is the overall checkout abandonment rate?",
    "Which device has the highest checkout abandonment?",
    "Which acquisition channel has the highest abandonment rate?",
    "What are the main conversion issues in the funnel?",
]

cols = st.columns(2)

for i, question in enumerate(example_questions):

    with cols[i % 2]:

        if st.button(
            question,
            use_container_width=True,
            key=f"example_{i}",
        ):
            st.session_state.ai_question = question


st.divider()


# =========================
# Chat History
# =========================

for message in st.session_state.ai_messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# =========================
# User Input
# =========================

user_question = st.chat_input(
    "Ask a question about your GA4 data..."
)

# If user clicked an example question
if "ai_question" in st.session_state:

    user_question = st.session_state.ai_question

    del st.session_state.ai_question


# =========================
# Run Agent
# =========================

if user_question:

    # Display user message
    with st.chat_message("user"):
        st.markdown(user_question)

    st.session_state.ai_messages.append(
        {
            "role": "user",
            "content": user_question,
        }
    )

    # General analytics prompt
    question = user_question

    # Run Agent
    with st.chat_message("assistant"):

        with st.spinner("🤖 AI Analyst is analysing the data..."):

            try:

                response, tool_results = run_agent(
                    question=question,
                    tools=tools,
                )

                answer = response.text

            except Exception as error:

                answer = (
                    "I could not complete the analysis because "
                    f"an error occurred: {error}"
                )

        st.markdown(answer)

    # Save assistant response
    st.session_state.ai_messages.append(
        {
            "role": "assistant",
            "content": answer,
        }
    )