# Business Problem – Retail Customer Churn Analytics

## Background

In the Retail & Consumer domain, customer churn is often silent.
Customers do not formally cancel; instead, they gradually stop purchasing.
This makes churn difficult to detect until revenue has already been lost.

Retail organizations therefore need a predictive, data-driven approach to identify customers who are likely to disengage before churn actually occurs.

---

## Business Objective

The objective of this project is to predict which customers are at risk of churning in the near future, so that marketing and CRM teams can proactively intervene with targeted retention strategies.

---

## Definition of Churn

A customer is considered churned if they:

- Were active during the recent observation period, and
- Make no purchase in the subsequent 30 days

This definition reflects how churn is typically measured in Retail & Consumer businesses, where inactivity is the primary signal of disengagement.

---

## Prediction Framing

- **Observation Window:** Last 90 days of customer behavior
- **Prediction Window:** Next 30 days
- **Prediction Target:** Binary churn flag (1 = churn, 0 = retained)

All features are derived strictly from data available before the prediction window to prevent data leakage.

---

## Key Business Questions

This project aims to answer:

1. Which customers are most likely to stop purchasing in the near future?
2. What behavioral signals (recency, frequency, spend, engagement) drive churn?
3. How can limited retention budgets be allocated to maximize impact?

---

## Business Users

The outputs of this model are intended for:

- CRM & Lifecycle Marketing teams
- Customer Analytics teams
- Growth & Retention stakeholders

---

## Business Action

The model is designed to support targeted retention campaigns, such as:

- Win-back emails for inactive customers
- Personalized discounts for low-spend customers
- Loyalty incentives for declining engagement

Because retention budgets are limited, the model prioritizes ranking customers by churn risk, enabling the business to focus on the top-risk segment.

---

## Success Metrics

Model success is evaluated using:

- PR-AUC (to handle class imbalance)
- Lift @ Top 10% customers, measuring improvement over random targeting

These metrics align with real-world retail decision-making, where only a subset of customers can be contacted.

---

## Expected Impact

By identifying high-risk customers earlier, this solution enables:

- More efficient use of retention budgets
- Improved customer lifetime value
- Reduced revenue loss from silent churn

---

## Summary

This project translates raw retail transaction data into actionable churn insights, combining predictive modeling, explainability, and deployment-ready architecture to support real business decisions.
