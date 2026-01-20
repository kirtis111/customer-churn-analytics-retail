from fastapi import FastAPI
from fastapi import HTTPException
from app.schemas import PredictRequest, PredictResponse, PredictBatchRequest
from app.model import ChurnModelService

app = FastAPI(
    title="Retail Churn Prediction API",
    version="1.0.0",
    description="FastAPI service to score retail customers for churn risk using an XGBoost model."
)

service = ChurnModelService()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict", response_model=PredictResponse)
def predict(req: PredictRequest):
    proba = service.predict_proba(req.features.model_dump())
    return PredictResponse(customer_id=req.customer_id, churn_probability=proba)


@app.post("/predict_batch")
def predict_batch(req: PredictBatchRequest):
    results = []
    for item in req.items:
        proba = service.predict_proba(item.features.model_dump())
        results.append({"customer_id": item.customer_id, "churn_probability": proba})
    return {"results": results}

# ---------------------------Exception Handling------------------------------------

@app.post("/predict", response_model=PredictResponse)
def predict(req: PredictRequest):
    try:
        proba = service.predict_proba(req.features.model_dump())
        return PredictResponse(customer_id=req.customer_id, churn_probability=proba)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
