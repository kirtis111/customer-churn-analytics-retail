# Data Dictionary – Retail Customer Churn Analytics

This document describes the variables used in the customer-level modeling dataset (`modeling_table.csv`) for the Retail Customer Churn Analytics project.

All features are derived from transactional data within a fixed observation window and are designed to capture customer purchasing behavior and engagement.

---

## Entity: Customer

Each row in the modeling dataset represents one unique customer.

---

## Target Variable

| Column Name | Type         | Description                                                                                                                                                                        |
| ----------- | ------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| churn       | Binary (0/1) | Target variable indicating whether the customer churned.`1` = customer made no purchase in the subsequent 30-day prediction window; `0` = customer made at least one purchase. |

---

## Identifier

| Column Name | Type    | Description                                                                                                      |
| ----------- | ------- | ---------------------------------------------------------------------------------------------------------------- |
| CustomerID  | Integer | Unique identifier for each customer. Used only for reference and joining datasets; excluded from model training. |

---

## Behavioral & RFM Features

| Column Name         | Type    | Description                                                                                                                                             |
| ------------------- | ------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- |
| recency_days        | Integer | Number of days since the customer’s most recent purchase at the end of the observation window. Higher values indicate longer inactivity.               |
| txn_count_90d       | Integer | Total number of transactions made by the customer during the 90-day observation window. Represents purchase frequency.                                  |
| spend_90d           | Float   | Total monetary value of purchases made by the customer during the observation window. Represents overall customer value.                                |
| avg_basket_value    | Float   | Average spend per transaction for the customer, calculated across all transactions in the observation window. Indicates basket depth.                   |
| unique_products_90d | Integer | Number of distinct products purchased by the customer during the observation window. Serves as a proxy for engagement and product exploration.          |
| country_count       | Integer | Number of unique countries associated with the customer’s transactions. Included to capture geographic diversity, though found to have limited impact. |

---

## Notes on Feature Usage

- All features are calculated only from data available before the prediction window to prevent data leakage.
- Features are aggregated at the customer level to support churn prediction and ranking.
- Categorical variables were excluded in favor of behavioral and monetary signals commonly used in retail churn analysis.

---

## Modeling Considerations

- The dataset exhibits a relatively high base churn rate, which is common in retail transaction data.
- Model evaluation focuses on ranking performance rather than accuracy, using PR-AUC and Lift@Top10%.
- Feature order is enforced during deployment using `feature_columns.json` to ensure consistency between training and inference.

---

## Summary

This data dictionary provides transparency into how customer behavior is represented in the churn prediction model and supports interpretability for both technical and non-technical stakeholders.
