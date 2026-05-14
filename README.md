# Telco Churn & Segmentation Project

This project predicts:
- Customer churn probability
- Customer segment

## Run locally with Docker
```bash
docker compose up --build
Services
FastAPI: http://localhost:8000/docs
Streamlit: http://localhost:8501

---

# 5. Very important notebook step before using this project

Make sure you saved the correct feature columns from your training notebook:

```python
import joblib
joblib.dump(X.columns.tolist(), 'models/feature_columns.pkl')
6. How the full system works
Flow
User enters customer info in Streamlit
Streamlit sends JSON to FastAPI /predict
FastAPI:
preprocesses raw input
prepares XGBoost input using feature_columns.pkl
predicts churn
creates clustering features
scales them with scaler_cluster.pkl
predicts segment with kmeans_model.pkl
FastAPI returns JSON
Streamlit shows result
7. How to run locally without Docker first

From project root:

Start API
uvicorn app.main:app --reload

Open:

http://127.0.0.1:8000/docs
Start Streamlit

Open another terminal:

streamlit run ui/streamlit_app.py

If running locally without Docker, change this line in ui/streamlit_app.py:

API_URL = "http://api:8000/predict"

to:

API_URL = "http://127.0.0.1:8000/predict"

For Docker Compose, keep http://api:8000/predict.

8. How to run with Docker

From project root:

docker compose up --build

Then open:

FastAPI docs: http://localhost:8000/docs
Streamlit UI: http://localhost:8501
9. What files in your current project are necessary
Necessary for runtime

Keep:

models/xgb_model.pkl
models/feature_columns.pkl
models/kmeans_model.pkl
models/scaler_cluster.pkl
Not necessary for runtime

These are optional:

outputs/*.png
outputs/customer_churn_predictions.csv
raw notebook charts
confusion matrix images
SHAP plots
ROC plots
CSV

data/WA_Fn-UseC_-Telco-Customer-Churn.csv is optional for deployment. Keep it for reference, but runtime doesn’t need it.

10. Final advice before you start

Follow this exact order:

Step 1

Create folders and files

Step 2

Put your .pkl files into models/

Step 3

Paste all backend code

Step 4

Test FastAPI in /docs

Step 5

Paste Streamlit code

Step 6

Run UI locally

Step 7

Dockerize and run compose