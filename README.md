# 📊 GA4 E-commerce Product Analytics & AI Analyst

> **End-to-end Product Analytics application** combining **Google Analytics 4, BigQuery, dbt, Python, Machine Learning, RAG, AI Tool Calling, Streamlit, Docker, and Google Cloud Run**.

This project investigates a core e-commerce product question:

> **Why do users abandon the checkout process, and can high-intent users be identified before they drop off?**

Starting from raw GA4 event data, the project builds a session-level analytics layer, analyzes the conversion funnel and checkout abandonment, predicts purchase intent with machine learning, and provides a conversational **AI Analyst** that can query analytical tools and retrieve project-specific knowledge.

---

## 🚀 Live Demo

| Resource | Link |
|---|---|
| 🌐 Streamlit App | [Open Live Demo](https://ga4-product-analytics-331058043654.europe-west9.run.app) |
| 📈 Tableau Dashboard | [View Dashboard](https://public.tableau.com/views/Book1_17830071008490/GA4E-commerceProductAnalytics?:language=en-US&publish=yes&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link) |
| 🎥 Presentation | [View Slides](https://prezi.com/view/545KkHZaM3tNWyV5iDGI/?referral_token=rRps2GlnB3FN) |

---

## 🎯 Business Problem

The project focuses on two connected product analytics objectives:

1. **Understand checkout abandonment**
   - Where do users drop off?
   - Which devices and acquisition channels show different abandonment patterns?
   - Which funnel stages have the largest conversion loss?

2. **Identify purchase intent**
   - Can session-level behavior be used to predict purchase probability?
   - Which behavioral features contribute most to the model?
   - How can predicted intent support product analysis and potential interventions?

A third layer was added to make the analytics more accessible:

3. **Enable conversational analytics**
   - Can a business user ask questions in natural language?
   - Can the AI retrieve current metrics through analytical tools rather than inventing numbers?
   - Can project definitions and methodology be retrieved through RAG?

---

## 📊 Dataset

The project uses **Google Analytics 4 event-level data** modeled at the session level.

| Metric | Value |
|---|---:|
| Events | 4,295,584 |
| Users | 270,154 |
| Sessions | 349,545 |
| Date range | 2020-11-01 → 2021-01-31 |
| Overall purchase conversion | 1.39% |
| Completed purchases | 4,845 |
| Checkout abandonment rate | 56.33% |

### Important metric definition

The project distinguishes between overall purchases and purchases among checkout sessions:

- **4,845** sessions are recorded as purchases across the full funnel.
- **11,088** sessions initiated checkout.
- **6,246** checkout sessions were abandoned.
- The checkout abandonment rate is **56.33%**.

The AI Analyst retrieves these metrics from the analytical layer rather than storing the current KPI as a hard-coded value.

---

# 🏗️ Architecture

```text
                 GA4 Event Data
                       │
                       ▼
                Google BigQuery
                       │
                       ▼
                     dbt
        ┌──────────────┼──────────────┐
        ▼              ▼              ▼
     Staging      Intermediate       Marts
                     │
                     ▼
               int_sessions
                     │
          ┌──────────┼───────────┐
          ▼          ▼           ▼
       Funnel     Checkout       ML
      Analytics   Analytics   Prediction
          │          │           │
          └──────────┼───────────┘
                     │
                     ▼
                Streamlit App
                     │
        ┌────────────┼────────────┐
        ▼            ▼            ▼
      Funnel      Checkout    Prediction
                     │
                     ▼
                AI Analyst
              ┌──────┴──────┐
              ▼             ▼
       Analytics Tools      RAG
              │             │
              └──────┬──────┘
                     ▼
                  Gemini
                     │
                     ▼
                 Docker
                     │
                     ▼
               Google Cloud Run
```

---

# 🛠️ Tech Stack

| Category | Technologies |
|---|---|
| Analytics source | Google Analytics 4 |
| Data warehouse | Google BigQuery |
| Data transformation | dbt |
| Programming | Python |
| Data analysis | Pandas, NumPy |
| Machine learning | Scikit-learn, Random Forest, XGBoost |
| LLM | Google Gemini |
| AI architecture | Function / Tool Calling, RAG |
| Embeddings | Gemini Embeddings |
| Local LLM option | Ollama |
| Visualization | Plotly, Tableau |
| Application | Streamlit |
| Containerization | Docker |
| Cloud deployment | Google Cloud Run |
| Secrets | Google Secret Manager |

---

# 📂 Project Structure

```text
.
├── app/
│   ├── Home.py
│   ├── pages/
│   │   ├── 01_Funnel.py
│   │   ├── 02_Checkout.py
│   │   ├── 03_Prediction.py
│   │   └── 04_AI_Analyst.py
│   └── assets/
│
├── ai/
│   ├── tools/
│   │   ├── analyst.py
│   │   ├── rag.py
│   │   ├── schemas.py
│   │   └── definitions.py
│   ├── rag/
│   │   ├── loader.py
│   │   ├── chunker.py
│   │   ├── embedding.py
│   │   ├── retriever.py
│   │   └── vector_store.py
│   ├── providers/
│   │   ├── base.py
│   │   ├── gemini.py
│   │   └── ollama.py
│   ├── llm.py
│   ├── prompts.py
│   └── tool_calling.py
│
├── dbt/
│   ├── models/
│   │   ├── staging/
│   │   ├── intermediate/
│   │   └── marts/
│   └── dbt_project.yml
│
├── notebooks/
│   ├── 01_data_understanding.ipynb
│   ├── 02_product_analysis.ipynb
│   └── 03_purchase_intent_prediction.ipynb
│
├── models/
│   ├── baseline_model.pkl
│   ├── rf_model.pkl
│   ├── tuned_rf_model.pkl
│   └── xgb_model.pkl
│
├── outputs/
│   ├── model_comparison.csv
│   ├── feature_importance.csv
│   └── RAG / agent evaluation outputs
│
├── src/
│   ├── config.py
│   ├── database.py
│   ├── queries.py
│   └── services.py
│
├── tableau/
├── sql/
├── Dockerfile
├── pyproject.toml
└── README.md
```

---

# 🔄 Data & Analytics Pipeline

## 1. GA4 → BigQuery

Raw GA4 event data is stored in BigQuery.

The analysis starts from event-level data and aggregates user interactions into session-level records.

## 2. dbt Modeling

The dbt project follows a layered structure:

```text
Staging
   ↓
Intermediate
   ↓
Marts
```

### Staging

`stg_events`

- Cleans raw GA4 events
- Extracts event parameters
- Standardizes the analytical schema

### Intermediate

`int_sessions`

Creates one analytical record per session, including:

- Session duration
- Total events
- Engagement
- Page views
- Product views
- Searches
- Add-to-cart activity
- Checkout initiation
- Purchase status
- Device
- Country
- Acquisition information

### Marts

- `mart_funnel`
- `mart_checkout_abandonment`
- `mart_purchase_prediction`
- `mart_kpi_summary`

These models provide reusable business-ready datasets for dashboards, machine learning, and AI tools.

---

# 📈 Product Analytics

The product analysis examines the complete e-commerce funnel:

```text
Page View
    ↓
View Item
    ↓
Add to Cart
    ↓
Begin Checkout
    ↓
Purchase
```

### Funnel Analysis

The Streamlit Funnel page provides:

- Funnel visualization
- Overall conversion rate
- Stage-to-stage conversion
- Stage drop-off
- Identification of the largest conversion-loss stage

The current analysis identifies **View Item → Add to Cart** as the largest funnel drop-off.

### Checkout Analysis

The Checkout page provides:

- Checkout sessions
- Purchase sessions
- Checkout abandonment rate
- Checkout funnel
- Completed vs abandoned sessions
- Behavioral comparison
- Device analysis
- Country analysis
- Acquisition-channel analysis

### Important analytical limitation

The project uses observational analytics data.

Therefore:

> **A higher abandonment rate for a device or acquisition channel does not by itself establish why users abandon checkout.**

Causal explanations would require additional evidence such as experiments, user research, qualitative feedback, or other behavioral data.

---

# 🤖 Purchase Intent Prediction

The project predicts purchase probability at the **session level**.

### Models evaluated

- Logistic Regression
- Random Forest
- Tuned Random Forest
- XGBoost

### Feature engineering

The model includes behavioral and contextual features such as:

- Session duration
- Total events
- Engagement time
- Page views
- Unique pages
- Item views
- Searches
- Add to cart
- Begin checkout
- Engagement per event
- Item view rate
- Checkout ratio
- Device
- Operating system
- Country
- Acquisition channel

### Model comparison

| Model | Accuracy | Precision | Recall | F1 | ROC-AUC |
|---|---:|---:|---:|---:|---:|
| Logistic Regression | 0.706 | 0.695 | 0.608 | 0.649 | 0.802 |
| Random Forest | 0.728 | 0.682 | 0.732 | 0.706 | 0.805 |
| **Tuned Random Forest** | **0.737** | **0.686** | **0.760** | **0.721** | 0.811 |
| XGBoost | 0.733 | 0.692 | 0.727 | 0.709 | **0.817** |

The **Tuned Random Forest** is the model deployed for the interactive prediction experience.

The model output is a **predicted purchase probability**, not an actual purchase outcome.

---

# 🧠 AI Analyst

The project includes a conversational AI Analyst designed specifically for product analytics.

Instead of asking the LLM to generate answers from memory, the agent can call structured analytical tools and retrieve project-specific documentation.

### Analytics tools

The agent can use tools for:

- Checkout abandonment KPIs
- Funnel metrics
- Abandonment by device
- Abandonment by acquisition channel
- Session-level purchase prediction

### RAG knowledge search

A lightweight RAG pipeline provides project-specific context from:

```text
ai/knowledge/
├── business_context.md
├── funnel_definition.md
└── metrics_definition.md
```

The RAG pipeline:

```text
User Question
     ↓
Embedding
     ↓
Vector Retrieval
     ↓
Relevant Project Knowledge
     ↓
Gemini
```

Embeddings are stored by embedding model so that different providers/models can maintain separate vector stores.

### Tool Calling + RAG

For questions requiring both documentation and data, the agent can combine both:

```text
User Question
      ↓
    Gemini
      │
      ├── Analytics Tool
      │       ↓
      │   BigQuery / dbt data
      │
      └── RAG Tool
              ↓
        Project knowledge
      │
      └──────────────┐
                     ▼
                Final Answer
```

### Grounding principles

The AI Analyst is explicitly instructed to:

- Use analytical tools for numerical GA4 metrics
- Use RAG for project definitions and methodology
- Treat tool results as the source of truth for numerical values
- Avoid inventing metrics
- Avoid inventing user motivations
- Avoid claiming causality from observational data
- Clearly distinguish observed data from model predictions
- State when the available evidence is insufficient

### Example questions

```text
What is the overall checkout abandonment rate?

Which device has the highest checkout abandonment?

Which acquisition channel has the highest abandonment rate?

What are the main conversion issues in the funnel?

Why are users abandoning checkout?
```

For causal "why" questions, the agent does not automatically convert descriptive correlations into causal explanations.

---

# 🖥️ Streamlit Application

The application contains four main analytical experiences.

## 🏠 Home

Executive overview including:

- Users
- Sessions
- Purchases
- Conversion
- Funnel overview
- Device distribution
- Traffic sources
- Countries
- Quick product insights

## 📈 Funnel Analysis

Explore the complete purchase funnel and identify conversion bottlenecks.

## 🛒 Checkout Analysis

Analyze checkout completion and abandonment across behavioral and user segments.

## 🤖 Purchase Intent Prediction

Enter a GA4 session ID to retrieve:

- Purchase prediction
- Predicted purchase probability
- Session characteristics
- Engineered behavioral features
- AI-generated interpretation

## 🧠 AI Analyst

Ask natural-language questions about the project's GA4 product analytics data.

---

# 📊 Tableau Dashboard

The Tableau Public dashboard provides an executive-level view of the product analytics dataset.

It includes:

- Executive KPIs
- Purchase funnel
- Device analysis
- Traffic source analysis
- Geographic distribution
- Interactive filters

**Tableau:** [View Tableau Dashboard](https://public.tableau.com/views/Book1_17830071008490/GA4E-commerceProductAnalytics?:language=en-US&publish=yes&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link)

---

# ☁️ Deployment

The Streamlit application is containerized with Docker and deployed to Google Cloud Run.

```text
Python Application
       ↓
     Docker
       ↓
Artifact Registry
       ↓
 Google Cloud Run
       ↓
 Public Streamlit Application
```

The current deployment uses:

- Google Cloud Run
- Artifact Registry
- Google BigQuery
- Gemini API
- Google Secret Manager

The Gemini API key is stored as a Secret Manager secret and exposed to the Cloud Run service at runtime rather than being included in the Docker image or repository.

### Local Docker test

```bash
docker build --platform linux/amd64 -t ga4-product-analytics .

docker run --rm \
  --env-file .env \
  -v "$HOME/.config/gcloud:/root/.config/gcloud:ro" \
  -p 8080:8080 \
  ga4-product-analytics
```

### Cloud Run

Live application: [Open Live Demo](https://ga4-product-analytics-331058043654.europe-west9.run.app)

---

# ⚙️ Local Setup

## Requirements

- Python 3.11+
- Google Cloud / BigQuery access
- `uv`
- Gemini API key for the Gemini provider
- Ollama is optional for local LLM experimentation

## Install dependencies

```bash
uv sync
```

## Environment variables

Create a local `.env` file:

```env
LLM_PROVIDER=gemini
GEMINI_API_KEY=your_api_key
EMBEDDING_MODEL=gemini-embedding-001
```

For local Ollama experimentation:

```env
LLM_PROVIDER=ollama
EMBEDDING_MODEL=nomic-embed-text
```

Never commit `.env` or API keys to GitHub.

## Run Streamlit

```bash
streamlit run app/Home.py
```

---

# 🧪 AI Evaluation

The repository includes AI tests and evaluation cases under:

```text
ai/tests/
```

and recorded agent evaluation outputs under:

```text
outputs/agent_tests/
```

The AI Analyst was tested against:

- Numerical KPI questions
- Device and acquisition breakdowns
- Multi-tool questions
- Project-definition questions
- RAG retrieval
- Causal "why" questions
- Purchase prediction queries

---

# 📌 Key Findings

- **4,295,584** GA4 events were analyzed across **349,545 sessions**.
- Overall purchase conversion is **1.39%**.
- **11,088** sessions initiated checkout.
- **6,246** checkout sessions were abandoned, giving a **56.33%** checkout abandonment rate.
- The largest funnel conversion loss occurs between **View Item and Add to Cart**.
- Desktop has the highest checkout abandonment rate among the analyzed device categories at **56.95%**.
- Engagement and behavioral features are important inputs to the purchase-intent model.
- The AI Analyst can retrieve current analytics metrics and project-specific definitions through tool calling and RAG.
- Observational analytics alone is not sufficient to establish the causal reasons behind checkout abandonment.

---

# 🔮 Future Improvements

Potential extensions include:

- Real-time GA4 streaming with BigQuery
- Controlled A/B testing for checkout optimization
- Customer Lifetime Value prediction
- Product recommendation system
- SHAP-based model explainability
- Dedicated FastAPI prediction service
- CI/CD with GitHub Actions
- Expanded qualitative/user-research data for causal analysis
- More advanced conversational analytics and multi-step investigation workflows

---

# 👤 Author

**Zhiwen MO**

Product Analytics • Data Analytics • Machine Learning • AI Analytics • Business Intelligence
