# Business Context

## Project

This project is a product analytics solution for an e-commerce application based on Google Analytics 4 (GA4) event data.

The project combines:

- GA4 event data
- BigQuery
- dbt
- SQL
- Python
- Machine learning
- Streamlit

The analytics layer is designed to understand user behavior throughout the e-commerce funnel.

## Business Question

The main business question is:

> Why do users abandon the checkout process, and can high-intent users be identified before they drop off?

The project focuses on two related objectives:

1. Analyze checkout abandonment and identify patterns in user behavior.
2. Predict purchase intent at the session level using machine learning.

## Data Source

The project uses Google Analytics 4 event-level data.

The analysis is performed at the session level after transforming and modeling the event data with dbt.

The main analytical models include:

- `int_sessions`
- `mart_funnel`
- `mart_checkout_abandonment`
- `mart_purchase_prediction`

## Analytical Scope

The project analyzes:

- E-commerce funnel progression
- Checkout abandonment
- Acquisition channels
- Device categories
- Session behavior
- Purchase behavior
- Purchase intent prediction

## Limitations

The available data is observational analytics data.

Descriptive relationships between metrics, devices, acquisition channels, and checkout abandonment do not establish causality.

For example, a higher abandonment rate for a particular device or acquisition channel does not by itself explain why users abandoned checkout.

Additional evidence such as controlled experiments, user research, qualitative feedback, or other behavioral data would be required to establish causal explanations.

Machine learning predictions represent model outputs and should not be interpreted as actual purchase outcomes.