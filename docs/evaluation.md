# Model Evaluation – Retail Customer Churn Analytics

## Evaluation Objectives

The goal of model evaluation in this project is to assess how effectively the model can rank customers by churn risk and support targeted retention decisions, rather than simply maximizing classification accuracy.

Given the business context, evaluation emphasizes ranking quality, interpretability, and business impact.

---

## Dataset Characteristics

The dataset exhibits a relatively high base churn rate (~57%), which is common in retail transaction data where churn manifests as inactivity rather than explicit cancellation.

Because of this:

- Accuracy is not a meaningful metric
- Artificial rebalancing (e.g., oversampling) was avoided
- The model focuses on prioritizing high-risk customers

---

## Evaluation Metrics

### ROC-AUC

ROC-AUC is used to measure overall ranking performance across all classification thresholds.

- Logistic Regression: ~0.64
- XGBoost: ~0.67

This improvement indicates that the XGBoost model better distinguishes between churned and retained customers.

---

### PR-AUC

PR-AUC is emphasized due to the high churn prevalence and class imbalance.

- Logistic Regression: ~0.66
- XGBoost: ~0.69

The improvement in PR-AUC shows that the model more effectively identifies true churners among high-risk predictions.

---

### Lift @ Top 10%

Lift@10% is the primary business-aligned metric.

- **Base churn rate:** ~57%
- **Top 10% churn rate (XGBoost):** ~72%
- **Lift@10%:** ~1.27

This means that by targeting only the top 10% highest-risk customers, the business can identify **~27% more churners** compared to random selection.

Given the high base churn rate, this represents a meaningful improvement in targeting efficiency.

---

## Model Comparison Summary

| Model               | ROC-AUC | PR-AUC | Lift@10% |
| ------------------- | ------- | ------ | -------- |
| Logistic Regression | ~0.64   | ~0.66  | ~1.12    |
| XGBoost             | ~0.67   | ~0.69  | ~1.27    |

XGBoost consistently outperforms the baseline across all evaluation dimensions and is selected as the final model.

---

## Explainability and Business Validation

### Converting SHAP into Business Insights

SHAP analysis was used to validate that the model’s behavior aligns with known retail dynamics and to translate predictions into actionable insights.

#### Key Drivers of Churn

1. High Recency (days since last purchase) - Customers who have not purchased recently are significantly more likely to churn.
2. Low Purchase Frequency - Customers with fewer transactions during the observation window exhibit elevated churn risk.
3. Lower Monetary Value - Reduced spending and smaller basket sizes correlate with disengagement.
4. Limited Product Diversity - Customers purchasing from fewer product categories churn more often.

These drivers are intuitive, stable, and consistent with established retail churn patterns.

---

## Business Interpretation

The evaluation results demonstrate that the model:

- Reliably ranks customers by churn risk
- Identifies behaviorally disengaging customers early
- Supports targeted retention strategies under budget constraints

Rather than predicting churn in isolation, the model enables prioritization, which is the core requirement for real-world retail retention campaigns.

---

## Limitations

- High base churn rate naturally constrains maximum achievable lift
- Model relies solely on transactional data; additional engagement signals could further improve performance
- Lift is evaluated at a fixed threshold (Top 10%) and may vary with business capacity

These limitations are documented to ensure transparency and realistic expectations.

---

## Summary

The final XGBoost model delivers consistent improvements over baseline, strong explainability, and measurable business impact.
Evaluation results confirm that the model is suitable for deployment in retail churn use cases where early identification and prioritization of at-risk customers are critical.
