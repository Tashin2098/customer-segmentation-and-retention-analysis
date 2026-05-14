from pydantic import BaseModel
from typing import Literal


class CustomerInput(BaseModel):
    gender: Literal["Male", "Female"]
    SeniorCitizen: Literal["Yes", "No"]
    Partner: Literal["Yes", "No"]
    Dependents: Literal["Yes", "No"]
    tenure: float
    PhoneService: Literal["Yes", "No"]
    MultipleLines: Literal["No", "Yes", "No phone service"]
    InternetService: Literal["DSL", "Fiber optic", "No"]
    OnlineSecurity: Literal["No", "Yes", "No internet service"]
    OnlineBackup: Literal["No", "Yes", "No internet service"]
    DeviceProtection: Literal["No", "Yes", "No internet service"]
    TechSupport: Literal["No", "Yes", "No internet service"]
    StreamingTV: Literal["No", "Yes", "No internet service"]
    StreamingMovies: Literal["No", "Yes", "No internet service"]
    Contract: Literal["Month-to-month", "One year", "Two year"]
    PaperlessBilling: Literal["Yes", "No"]
    PaymentMethod: Literal[
        "Electronic check",
        "Mailed check",
        "Bank transfer (automatic)",
        "Credit card (automatic)"
    ]
    MonthlyCharges: float
    TotalCharges: float


class PredictionResponse(BaseModel):
    churn_probability: float
    churn_prediction: int
    prediction_label: str
    threshold_used: float
    risk_level: str
    segment: int
    segment_name: str
    risk_factors: list[str]
    protective_factors: list[str]
    retention_priority: str
    recommended_actions: list[str]