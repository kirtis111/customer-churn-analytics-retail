from pydantic import BaseModel, Field
from typing import List


class CustomerFeatures(BaseModel):
    # Keep names EXACTLY as training columns
    spend_90d: float = Field(..., ge=0)
    avg_basket_value: float = Field(..., ge=0)
    txn_count_90d: int = Field(..., ge=0)
    recency_days: int = Field(..., ge=0)
    unique_products_90d: int = Field(..., ge=0)
    country_count: int = Field(..., ge=0)


class PredictRequest(BaseModel):
    customer_id: int
    features: CustomerFeatures


class PredictResponse(BaseModel):
    customer_id: int
    churn_probability: float


class PredictBatchRequest(BaseModel):
    items: List[PredictRequest]
