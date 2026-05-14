import os
import streamlit as st
import requests

API_URL = os.getenv("API_URL", "http://api:8000/predict")

st.set_page_config(
    page_title="Telco Churn Predictor",
    layout="wide"
)

st.title("Telco Customer Churn & Segment Predictor")
st.write(
    "Enter customer information to predict churn risk, identify customer segment, "
    "understand key risk factors, and generate retention recommendations."
)

col1, col2 = st.columns(2)

with col1:
    gender = st.selectbox("Gender", ["Male", "Female"])
    senior = st.selectbox("Senior Citizen", ["No", "Yes"])
    partner = st.selectbox("Partner", ["No", "Yes"])
    dependents = st.selectbox("Dependents", ["No", "Yes"])
    tenure = st.slider("Tenure (months)", 0, 72, 12)

    phone_service = st.selectbox("Phone Service", ["Yes", "No"])

    if phone_service == "No":
        multiple_lines = "No phone service"
        st.selectbox("Multiple Lines", ["No phone service"], disabled=True)
    else:
        multiple_lines = st.selectbox("Multiple Lines", ["No", "Yes"])

    internet_service = st.selectbox("Internet Service", ["DSL", "Fiber optic", "No"])

    if internet_service == "No":
        online_security = "No internet service"
        online_backup = "No internet service"
        st.selectbox("Online Security", ["No internet service"], disabled=True)
        st.selectbox("Online Backup", ["No internet service"], disabled=True)
    else:
        online_security = st.selectbox("Online Security", ["No", "Yes"])
        online_backup = st.selectbox("Online Backup", ["No", "Yes"])

with col2:
    if internet_service == "No":
        device_protection = "No internet service"
        tech_support = "No internet service"
        streaming_tv = "No internet service"
        streaming_movies = "No internet service"

        st.selectbox("Device Protection", ["No internet service"], disabled=True)
        st.selectbox("Tech Support", ["No internet service"], disabled=True)
        st.selectbox("Streaming TV", ["No internet service"], disabled=True)
        st.selectbox("Streaming Movies", ["No internet service"], disabled=True)
    else:
        device_protection = st.selectbox("Device Protection", ["No", "Yes"])
        tech_support = st.selectbox("Tech Support", ["No", "Yes"])
        streaming_tv = st.selectbox("Streaming TV", ["No", "Yes"])
        streaming_movies = st.selectbox("Streaming Movies", ["No", "Yes"])

    contract = st.selectbox("Contract", ["Month-to-month", "One year", "Two year"])
    paperless_billing = st.selectbox("Paperless Billing", ["No", "Yes"])

    payment_method = st.selectbox(
        "Payment Method",
        [
            "Electronic check",
            "Mailed check",
            "Bank transfer (automatic)",
            "Credit card (automatic)"
        ]
    )

    monthly_charges = st.number_input(
        "Monthly Charges",
        min_value=0.0,
        value=70.0,
        step=1.0
    )

    total_charges = st.number_input(
        "Total Charges",
        min_value=0.0,
        value=500.0,
        step=1.0
    )

if st.button("Predict"):
    payload = {
        "gender": gender,
        "SeniorCitizen": senior,
        "Partner": partner,
        "Dependents": dependents,
        "tenure": tenure,
        "PhoneService": phone_service,
        "MultipleLines": multiple_lines,
        "InternetService": internet_service,
        "OnlineSecurity": online_security,
        "OnlineBackup": online_backup,
        "DeviceProtection": device_protection,
        "TechSupport": tech_support,
        "StreamingTV": streaming_tv,
        "StreamingMovies": streaming_movies,
        "Contract": contract,
        "PaperlessBilling": paperless_billing,
        "PaymentMethod": payment_method,
        "MonthlyCharges": monthly_charges,
        "TotalCharges": total_charges
    }

    try:
        response = requests.post(API_URL, json=payload, timeout=30)
        response.raise_for_status()
        result = response.json()

        st.subheader("Prediction Result")

        c1, c2, c3, c4 = st.columns(4)

        c1.metric("Churn Probability", f"{result['churn_probability']:.2%}")
        c2.metric("Prediction", result["prediction_label"])
        c3.metric("Risk Level", result["risk_level"])
        c4.metric("Segment", result["segment"])

        st.caption(f"Threshold used: {result['threshold_used']:.2f}")
        st.info(f"Customer Segment: {result['segment_name']}")

        if result["risk_level"] == "Critical":
            st.error("Critical churn risk. Immediate retention action is recommended.")
        elif result["risk_level"] == "High":
            st.warning("High churn risk. Proactive customer engagement is recommended.")
        elif result["risk_level"] == "Medium":
            st.info("Medium churn risk. Monitor the customer and consider targeted engagement.")
        else:
            st.success("Low churn risk. Customer appears relatively stable.")

        st.divider()

        st.subheader("Why this prediction?")

        col_risk, col_protect = st.columns(2)

        with col_risk:
            st.markdown("### Risk Factors")
            if result["risk_factors"]:
                for factor in result["risk_factors"]:
                    st.write(f"🔴 {factor}")
            else:
                st.write("No major risk factors detected.")

        with col_protect:
            st.markdown("### Protective Factors")
            if result["protective_factors"]:
                for factor in result["protective_factors"]:
                    st.write(f"🟢 {factor}")
            else:
                st.write("No strong protective factors detected.")

        st.divider()

        st.subheader("Recommended Retention Strategy")
        st.write(f"**Priority:** {result['retention_priority']}")

        for action in result["recommended_actions"]:
            st.write(f"✅ {action}")

    except requests.exceptions.RequestException as e:
        st.error(f"API request failed: {e}")