# Modeling Plan – Retail Customer Churn Analytics

## Objective

The goal of this modeling effort is to predict customer churn risk in the near future using historical retail transaction data and to rank customers by likelihood of churn to support targeted retention strategies.

The emphasis is on practical business impact, explainability, and deployability rather than purely optimizing accuracy.

---

## Problem Framing

- **Task Type:** Binary classification (churn vs. retained)
- **Primary Use Case:** Customer ranking for targeted retention
- **Domain:** Retail & Consumer

Given limited marketing budgets, the model is designed to prioritizehigh-risk customers rather than maximize overall classification accuracy.

---

## Churn Definition

A customer is labeled as churned if they:

- Were active during the observation window, and
- Made no purchase in the subsequent 30-day prediction window

This definition aligns with real-world retail churn, where churn manifests as inactivity rather than explicit cancellation.

---

## Data Preparation Strategy

### Observation & Prediction Windows

- **Observation Window:** Last 90 days of customer behavior
- **Prediction Window:** Next 30 days

All features are computed strictly from the observation window to prevent data leakage.

### Unit of Modeling

- One row per customer
- Aggregated behavioral and monetary features

---

## Feature Strategy

The model uses RFM-style and behavioral features commonly applied in retail analytics:

- **Recency:** Time since last purchase
- **Frequency:** Number of transactions
- **Monetary Value:** Total and average spend
- **Engagement:** Product diversity and basket behavior

Feature selection favors:

- Interpretability
- Stability over time
- Business relevance

No demographic or personally identifiable information is used.

---

## Modeling Approach

### Baseline Model

**Logistic Regression**

- Serves as an interpretable baseline
- Establishes a performance reference point
- Useful for validating feature signal

### Advanced Model

**XGBoost (Gradient Boosted Trees)**

- Captures non-linear relationships and feature interactions
- Well-suited for tabular retail data
- Balances performance with explainability

---

## Evaluation Strategy

### Why Accuracy Is Not Used

Accuracy is not an appropriate metric due to:

- Class imbalance
- High base churn rate
- Business focus on ranking, not exact classification

### Primary Evaluation Metrics

- **ROC-AUC:** Overall ranking performance
- **PR-AUC:** Performance under class imbalance
- **Lift @ Top 10%:** Business-aligned metric measuring improvement over random targeting

Lift is prioritized because retention teams typically engage only a fraction of customers.

---

## Model Selection Criteria

The final model is selected based on:

1. Improvement over baseline
2. Stability across metrics
3. Business interpretability
4. Compatibility with deployment and monitoring

XGBoost is selected as the final model due to consistent improvements in PR-AUC and Lift@10%.

---

## Explainability Plan

### Global Explainability

- SHAP summary plots are used to identify key churn drivers across the population.

### Individual Explainability

- SHAP waterfall plots are used to explain churn risk for individual customers.

Explainability ensures that model outputs can be translated into actionable business decisions.

---

## Deployment Considerations

- Model is deployed via FastAPI as an inference service.
- Feature order is enforced using a saved `feature_columns.json` file to prevent training–serving skew.
- Streamlit consumes the API for demo and batch scoring use cases.

This separation supports scalability and reuse in production systems.

---

## Risks & Limitations

- High base churn rate naturally limits maximum achievable lift.
- Model relies solely on transaction data; additional engagement signals (e.g., browsing behavior) could further improve performance.
- Churn definition is time-window dependent and may vary across retail contexts.

These limitations are documented to ensure transparency.

---

## Future Enhancements

Potential improvements include:

- Incorporating customer tenure and lifecycle stage
- Testing alternative ranking-optimized objectives
- Adding automated retraining and monitoring
- Extending API to accept raw transaction inputs

---

## Summary

This modeling plan balances predictive performance, business relevance, and deployment readiness, resulting in a churn prediction system suitable for real-world Retail & Consumer analytics use cases.
