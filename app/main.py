from fastapi import FastAPI, HTTPException
from app.schemas import CustomerInput, PredictionResponse
from app.predict import predict_customer

app = FastAPI(
    title="Telco Churn & Segmentation API",
    version="4.0.0"
)


@app.get("/")
def root():
    return {"message": "Telco Churn & Segmentation API is running"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict", response_model=PredictionResponse)
def predict(data: CustomerInput):
    try:
        result = predict_customer(data.model_dump())
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))