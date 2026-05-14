from pathlib import Path
import joblib
import pandas as pd

from app.utils import (
    convert_yes_no_fields,
    apply_feature_engineering,
    prepare_model_input,
    get_risk_level,
    get_segment_name,
    generate_explanation,
    generate_retention_recommendation
)

BASE_DIR = Path(__file__).resolve().parent.parent
MODELS_DIR = BASE_DIR / "models"

xgb_model = joblib.load(MODELS_DIR / "xgb_model.pkl")
feature_columns = joblib.load(MODELS_DIR / "feature_columns.pkl")
churn_threshold = joblib.load(MODELS_DIR / "churn_threshold.pkl")

kmeans_model = joblib.load(MODELS_DIR / "kmeans_model.pkl")
scaler_cluster = joblib.load(MODELS_DIR / "scaler_cluster.pkl")
clustering_features = joblib.load(MODELS_DIR / "clustering_features.pkl")


def predict_customer(payload: dict) -> dict:
    raw_df = pd.DataFrame([payload])

    engineered_df = apply_feature_engineering(raw_df)

    model_df = convert_yes_no_fields(engineered_df)
    model_input = prepare_model_input(model_df, feature_columns)

    churn_probability = float(xgb_model.predict_proba(model_input)[0][1])
    churn_prediction = int(churn_probability >= churn_threshold)

    cluster_input = engineered_df[clustering_features].fillna(0)
    cluster_scaled = scaler_cluster.transform(cluster_input)
    segment = int(kmeans_model.predict(cluster_scaled)[0])

    explanation = generate_explanation(payload, churn_probability)

    recommendation = generate_retention_recommendation(
        probability=churn_probability,
        segment=segment,
        payload=payload
    )

    return {
        "churn_probability": churn_probability,
        "churn_prediction": churn_prediction,
        "prediction_label": "Churn" if churn_prediction == 1 else "No Churn",
        "threshold_used": float(churn_threshold),
        "risk_level": get_risk_level(churn_probability),
        "segment": segment,
        "segment_name": get_segment_name(segment),
        "risk_factors": explanation["risk_factors"],
        "protective_factors": explanation["protective_factors"],
        "retention_priority": recommendation["retention_priority"],
        "recommended_actions": recommendation["recommended_actions"]
    }