import os
import json
import joblib
import pandas as pd
from typing import Dict, Any

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
MODEL_PATH = os.path.join(BASE_DIR, "models", "xgboost_model.pkl")
COLS_PATH = os.path.join(BASE_DIR, "models", "feature_columns.json")


class ChurnModelService:
    def __init__(self, model_path: str = MODEL_PATH, cols_path: str = COLS_PATH):
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file not found at: {model_path}")

        if not os.path.exists(cols_path):
            raise FileNotFoundError(
                f"feature_columns.json not found at: {cols_path}. "
                f"Create it from your training notebook."
            )

        self.model = joblib.load(model_path)

        with open(cols_path, "r") as f:
            self.feature_cols = json.load(f)

    def predict_proba(self, features: Dict[str, Any]) -> float:
        # Build a 1-row DataFrame from incoming JSON
        X = pd.DataFrame([features])

        # Enforce training columns + order; fill missing with 0 (optional safety)
        X = X.reindex(columns=self.feature_cols, fill_value=0)

        proba = float(self.model.predict_proba(X)[:, 1][0])
        return proba