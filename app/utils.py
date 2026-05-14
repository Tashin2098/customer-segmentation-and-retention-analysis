import pandas as pd


def convert_yes_no_fields(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    yes_no_cols = [
        "SeniorCitizen",
        "Partner",
        "Dependents",
        "PhoneService",
        "PaperlessBilling"
    ]

    for col in yes_no_cols:
        if col in df.columns:
            df[col] = df[col].map({"Yes": 1, "No": 0})

    if "gender" in df.columns:
        df["gender"] = df["gender"].map({"Male": 1, "Female": 0})

    numeric_cols = ["tenure", "MonthlyCharges", "TotalCharges"]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    return df


def apply_feature_engineering(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df["TotalCharges"] = pd.to_numeric(
        df["TotalCharges"],
        errors="coerce"
    ).fillna(0)

    df["Is_New_Customer"] = (df["tenure"] < 6).astype(int)
    df["Is_Early_Customer"] = ((df["tenure"] >= 6) & (df["tenure"] < 12)).astype(int)
    df["Is_Long_Term"] = (df["tenure"] >= 24).astype(int)

    df["Is_Month_to_Month"] = (df["Contract"] == "Month-to-month").astype(int)
    df["Has_Long_Contract"] = df["Contract"].isin(["One year", "Two year"]).astype(int)

    df["High_Monthly_Charge"] = (df["MonthlyCharges"] > 80).astype(int)
    df["Very_High_Monthly_Charge"] = (df["MonthlyCharges"] > 100).astype(int)

    df["Has_Fiber"] = (df["InternetService"] == "Fiber optic").astype(int)
    df["No_Internet"] = (df["InternetService"] == "No").astype(int)

    df["Has_TechSupport"] = (df["TechSupport"] == "Yes").astype(int)
    df["Has_OnlineSecurity"] = (df["OnlineSecurity"] == "Yes").astype(int)
    df["Has_OnlineBackup"] = (df["OnlineBackup"] == "Yes").astype(int)
    df["Has_DeviceProtection"] = (df["DeviceProtection"] == "Yes").astype(int)

    df["Uses_Electronic_Check"] = (df["PaymentMethod"] == "Electronic check").astype(int)
    df["Uses_AutoPay"] = df["PaymentMethod"].isin([
        "Bank transfer (automatic)",
        "Credit card (automatic)"
    ]).astype(int)

    service_cols = [
        "PhoneService",
        "OnlineSecurity",
        "OnlineBackup",
        "DeviceProtection",
        "TechSupport",
        "StreamingTV",
        "StreamingMovies"
    ]

    df["Service_Count"] = 0
    for col in service_cols:
        df["Service_Count"] += (df[col] == "Yes").astype(int)

    df["Engagement_Score"] = (
        df["Has_TechSupport"] +
        df["Has_OnlineSecurity"] +
        df["Has_OnlineBackup"] +
        df["Has_DeviceProtection"] +
        (df["StreamingTV"] == "Yes").astype(int) +
        (df["StreamingMovies"] == "Yes").astype(int)
    )

    df["New_Monthly_HighCharge"] = (
        df["Is_New_Customer"] *
        df["Is_Month_to_Month"] *
        df["High_Monthly_Charge"]
    )

    df["Fiber_HighCharge"] = (
        df["Has_Fiber"] *
        df["High_Monthly_Charge"]
    )

    df["NoSupport_Monthly"] = (
        (df["TechSupport"] == "No").astype(int) *
        df["Is_Month_to_Month"]
    )

    df["ElectronicCheck_Monthly"] = (
        df["Uses_Electronic_Check"] *
        df["Is_Month_to_Month"]
    )

    df["LowEngagement_HighCharge"] = (
        (df["Engagement_Score"] <= 1).astype(int) *
        df["High_Monthly_Charge"]
    )

    df["Avg_Charge_Per_Tenure"] = (
        df["TotalCharges"] / (df["tenure"] + 1)
    )

    df["Recency_Proxy"] = df["tenure"]
    df["Monetary"] = df["MonthlyCharges"]
    df["Support_Engagement"] = df["Engagement_Score"]

    df["Frequency_Proxy"] = df["InternetService"].map({
        "No": 0,
        "DSL": 1,
        "Fiber optic": 2
    }).fillna(0)

    return df


def prepare_model_input(df: pd.DataFrame, feature_columns: list[str]) -> pd.DataFrame:
    df = df.copy()
    df = pd.get_dummies(df, drop_first=True)

    for col in feature_columns:
        if col not in df.columns:
            df[col] = 0

    df = df[feature_columns]
    df = df.fillna(0)

    return df


def get_risk_level(probability: float) -> str:
    if probability >= 0.70:
        return "Critical"
    elif probability >= 0.50:
        return "High"
    elif probability >= 0.30:
        return "Medium"
    return "Low"


def get_segment_name(segment: int) -> str:
    segment_names = {
        0: "New High-Spend At-Risk Customers",
        1: "Loyal High-Engagement Customers",
        2: "Low-Value Stable Customers",
        3: "High-Spend Moderate-Engagement Customers",
        4: "New Low-Spend Customers"
    }

    return segment_names.get(segment, f"Segment {segment}")


def generate_explanation(payload: dict, probability: float) -> dict:
    risk_factors = []
    protective_factors = []

    if payload["tenure"] < 6:
        risk_factors.append(
            "Customer has very low tenure, meaning they are still in the early evaluation stage."
        )

    if payload["Contract"] == "Month-to-month":
        risk_factors.append(
            "Month-to-month contract allows the customer to leave easily."
        )

    if payload["MonthlyCharges"] > 80:
        risk_factors.append(
            "High monthly charge may create price sensitivity."
        )

    if payload["InternetService"] == "Fiber optic":
        risk_factors.append(
            "Fiber optic customers may have higher churn risk due to higher cost or service expectations."
        )

    if payload["TechSupport"] == "No":
        risk_factors.append(
            "No tech support may increase dissatisfaction risk."
        )

    if payload["OnlineSecurity"] == "No":
        risk_factors.append(
            "No online security indicates lower service engagement."
        )

    if payload["PaymentMethod"] == "Electronic check":
        risk_factors.append(
            "Electronic check payment is associated with higher churn risk."
        )

    if payload["tenure"] >= 24:
        protective_factors.append(
            "Long tenure indicates stronger customer loyalty."
        )

    if payload["Contract"] in ["One year", "Two year"]:
        protective_factors.append(
            "Long-term contract reduces churn risk."
        )

    if payload["TechSupport"] == "Yes":
        protective_factors.append(
            "Tech support increases customer support satisfaction."
        )

    if payload["OnlineSecurity"] == "Yes":
        protective_factors.append(
            "Online security indicates stronger service engagement."
        )

    if payload["OnlineBackup"] == "Yes":
        protective_factors.append(
            "Online backup shows additional service usage and engagement."
        )

    if payload["PaymentMethod"] in ["Credit card (automatic)", "Bank transfer (automatic)"]:
        protective_factors.append(
            "Automatic payment method usually indicates stable payment behavior."
        )

    return {
        "risk_factors": risk_factors,
        "protective_factors": protective_factors
    }


def generate_retention_recommendation(
    probability: float,
    segment: int,
    payload: dict
) -> dict:
    actions = []

    if probability >= 0.70:
        priority = "Critical"
        actions.append("Assign immediate proactive retention call.")
        actions.append("Offer personalized discount or loyalty benefit.")
        actions.append("Provide priority customer support follow-up.")

    elif probability >= 0.50:
        priority = "High"
        actions.append("Send targeted retention offer.")
        actions.append("Recommend service support or plan review.")
        actions.append("Monitor customer closely for the next billing cycle.")

    elif probability >= 0.30:
        priority = "Medium"
        actions.append("Send engagement message or value-added service offer.")
        actions.append("Monitor usage and billing behavior.")
        actions.append("Offer optional customer support check-in.")

    else:
        priority = "Low"
        actions.append("Maintain regular engagement.")
        actions.append("Promote loyalty or referral benefits.")
        actions.append("No urgent retention intervention required.")

    if payload["Contract"] == "Month-to-month":
        actions.append("Encourage migration to a one-year or two-year contract.")

    if payload["TechSupport"] == "No" and payload["InternetService"] != "No":
        actions.append("Offer free trial or discounted tech support.")

    if payload["OnlineSecurity"] == "No" and payload["InternetService"] != "No":
        actions.append("Recommend online security add-on to increase service engagement.")

    if payload["MonthlyCharges"] > 80:
        actions.append("Review pricing plan and suggest a better-value package.")

    if payload["PaymentMethod"] == "Electronic check":
        actions.append("Encourage switching to automatic payment for better account stability.")

    return {
        "retention_priority": priority,
        "recommended_actions": actions
    }