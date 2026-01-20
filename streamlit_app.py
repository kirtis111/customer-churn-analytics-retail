import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="Retail Churn Scoring", layout="wide")

API_BASE = st.sidebar.text_input("FastAPI Base URL", value="http://127.0.0.1:8000")

st.title("Retail Churn Prediction (Streamlit + FastAPI)")
st.caption("Scores customers for churn risk using deployed XGBoost model API.")

# ---------- Single prediction ----------
st.subheader("1) Single Customer Scoring")

with st.form("single_predict"):
    customer_id = st.number_input("Customer ID", min_value=0, value=12345, step=1)

    c1, c2, c3 = st.columns(3)
    with c1:
        spend_90d = st.number_input("spend_90d", min_value=0.0, value=120.5, step=1.0)
        avg_basket_value = st.number_input("avg_basket_value", min_value=0.0, value=30.1, step=1.0)
    with c2:
        txn_count_90d = st.number_input("txn_count_90d", min_value=0, value=6, step=1)
        recency_days = st.number_input("recency_days", min_value=0, value=12, step=1)
    with c3:
        unique_products_90d = st.number_input("unique_products_90d", min_value=0, value=18, step=1)
        country_count = st.number_input("country_count", min_value=0, value=1, step=1)

    submitted = st.form_submit_button("Predict churn probability")

if submitted:
    payload = {
        "customer_id": int(customer_id),
        "features": {
            "spend_90d": float(spend_90d),
            "avg_basket_value": float(avg_basket_value),
            "txn_count_90d": int(txn_count_90d),
            "recency_days": int(recency_days),
            "unique_products_90d": int(unique_products_90d),
            "country_count": int(country_count),
        },
    }

    try:
        r = requests.post(f"{API_BASE}/predict", json=payload, timeout=10)
        if r.status_code != 200:
            st.error(f"API error {r.status_code}: {r.text}")
        else:
            result = r.json()
            proba = float(result["churn_probability"])
            st.success(f"Churn probability: {proba:.3f}")

            # Simple interpretation helper
            if proba >= 0.70:
                st.warning("High risk: prioritize retention action.")
            elif proba >= 0.50:
                st.info("Medium risk: include in next campaign.")
            else:
                st.write("Lower risk: monitor or deprioritize.")
    except requests.RequestException as e:
        st.error(f"Could not reach API at {API_BASE}. Error: {e}")
        st.write("Tip: Start FastAPI with: uvicorn app.main:app --reload")

st.divider()

# ---------- Batch scoring ----------

st.subheader("2) Score from project dataset (modeling_table.csv)")

st.write("This loads processed modeling table and calls the FastAPI batch endpoint.")

default_path = "data/processed/modeling_table.csv"
modeling_path = st.text_input("Path to modeling_table.csv", value=default_path)

cA, cB, cC = st.columns(3)
with cA:
    max_rows = st.number_input("Max rows to score (for speed)", min_value=10, value=500, step=50)
with cB:
    sort_desc = st.selectbox("Sort output by", ["churn_probability (desc)", "customer_id (asc)"])
with cC:
    top_n = st.number_input("Show top N high-risk customers", min_value=10, value=50, step=10)

if st.button("Load and score from modeling_table.csv"):
    try:
        dfm = pd.read_csv(modeling_path)

        # Expect columns: CustomerID, churn, plus your engineered features
        # We will score using only feature columns (drop churn if present)
        if "CustomerID" not in dfm.columns:
            st.error("modeling_table.csv must contain a 'CustomerID' column.")
            st.stop()

        # Keep only feature columns your API expects
        required_feature_cols = [
            "spend_90d",
            "avg_basket_value",
            "txn_count_90d",
            "recency_days",
            "unique_products_90d",
            "country_count",
        ]
        missing_features = [c for c in required_feature_cols if c not in dfm.columns]
        if missing_features:
            st.error(f"Missing required feature columns in modeling_table.csv: {missing_features}")
            st.stop()

        # Optional: sample to keep batch requests fast
        dfm = dfm.head(int(max_rows)).copy()

        # Build items payload for FastAPI
        items = []
        for _, row in dfm.iterrows():
            items.append({
                "customer_id": int(row["CustomerID"]),
                "features": {
                    "spend_90d": float(row["spend_90d"]),
                    "avg_basket_value": float(row["avg_basket_value"]),
                    "txn_count_90d": int(row["txn_count_90d"]),
                    "recency_days": int(row["recency_days"]),
                    "unique_products_90d": int(row["unique_products_90d"]),
                    "country_count": int(row["country_count"]),
                }
            })

        r = requests.post(f"{API_BASE}/predict_batch", json={"items": items}, timeout=60)
        if r.status_code != 200:
            st.error(f"API error {r.status_code}: {r.text}")
            st.stop()

        results = pd.DataFrame(r.json()["results"])

        # Merge predictions back to view alongside optional churn label if present
        view_cols = ["CustomerID"]
        if "churn" in dfm.columns:
            view_cols.append("churn")

        df_out = dfm[view_cols].merge(
            results,
            left_on="CustomerID",
            right_on="customer_id",
            how="left"
        ).drop(columns=["customer_id"])

        # Sort
        if sort_desc == "churn_probability (desc)":
            df_out = df_out.sort_values("churn_probability", ascending=False)
        else:
            df_out = df_out.sort_values("CustomerID", ascending=True)

        st.success(f"Scored {len(df_out)} customers.")
        st.write(f"Top {int(top_n)} high-risk customers:")
        st.dataframe(df_out.head(int(top_n)), use_container_width=True)

        csv_bytes = df_out.to_csv(index=False).encode("utf-8")
        st.download_button(
            "Download scored customers CSV",
            data=csv_bytes,
            file_name="scored_customers_from_modeling_table.csv",
            mime="text/csv"
        )

    except FileNotFoundError:
        st.error(f"File not found: {modeling_path}")
        st.write("Tip: Ensure you run feature engineering and saved ../data/processed/modeling_table.csv")
    except Exception as e:
        st.error(f"Error: {e}")
