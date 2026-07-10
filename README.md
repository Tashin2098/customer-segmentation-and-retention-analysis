# Customer Segmentation and Retention Analysis

A machine learning project for telecom customer segmentation, churn prediction, and retention recommendation using XGBoost, K-Means, FastAPI, Streamlit, and Docker.

---

# Project Objective

The objective of this project is to build an end-to-end customer retention decision-support system for telecom businesses.

The system aims to:

- Predict whether a customer is likely to churn
- Estimate customer churn probability
- Segment customers into meaningful groups
- Identify key churn risk factors
- Recommend retention actions
- Provide a deployable API and user interface for practical use

---

# Purpose of the Project

Customer churn is a major challenge in the telecom industry. Acquiring new customers is often more expensive than retaining existing ones. If a company can identify at-risk customers early, it can take proactive actions such as offering better plans, improving support, or providing personalized retention offers.

This project was built to explore how machine learning can help telecom companies move from reactive customer retention to proactive customer retention.

---

# Dataset

This project uses the publicly available **Telco Customer Churn dataset** from Kaggle.

Dataset source:

https://www.kaggle.com/datasets/blastchar/telco-customer-churn

Dataset file used:

```text
WA_Fn-UseC_-Telco-Customer-Churn.csv
The dataset contains customer-level telecom information such as:

Customer demographics
Service subscriptions
Contract type
Payment method
Monthly charges
Total charges
Churn status
```

## Business Problem

Customer churn is a major challenge for telecom companies because losing existing customers directly affects revenue, customer lifetime value, and long-term business growth. Instead of reacting after customers leave, telecom businesses need a way to identify at-risk customers early and take proactive retention actions.

This project focuses on answering four key business questions:

- Which customers are likely to churn?
- What factors are contributing to their churn risk?
- What type of customer segment do they belong to?
- What retention action can be taken to reduce the risk?

By combining churn prediction, customer segmentation, and retention recommendation logic, this project aims to support more targeted and data-driven customer retention decisions.

## Community and Business Impact

This system can support telecom and subscription-based businesses by helping them make more proactive and data-driven customer retention decisions.

Potential business impacts include:

- Identifying at-risk customers early
- Reducing customer churn
- Improving customer satisfaction and engagement
- Supporting targeted retention campaigns
- Reducing unnecessary marketing costs
- Improving customer lifetime value
- Helping customer support teams prioritize high-risk users
- Enabling data-driven business decision-making

From a broader perspective, intelligent retention systems can help businesses provide more personalized and relevant customer experiences instead of relying on generic campaigns for all users.

---

## Machine Learning Approach

This project combines customer segmentation and churn prediction to better understand customer behavior and retention risk.

### 1. Customer Segmentation

K-Means clustering is used to group customers based on behavioral and service-related characteristics.

The segmentation process helps identify different types of customers, such as:

- New high-spend customers
- Loyal high-engagement customers
- Low-value stable customers
- High-spend moderate-engagement customers
- New low-spend customers

Customer segmentation helps businesses understand different customer groups and design more targeted retention strategies.

### 2. Churn Prediction

XGBoost is used to predict customer churn probability.

The model predicts:

- Churn probability
- Churn or no churn
- Risk level

The churn prediction pipeline includes:

- Data preprocessing
- Feature engineering
- Class imbalance handling
- Probability calibration
- Threshold tuning

---

## Key Features

The system provides:

- Customer churn prediction
- Churn probability estimation
- Customer risk classification
- Customer segmentation
- Segment naming and interpretation
- Risk factor identification
- Protective factor identification
- Retention recommendations
- FastAPI backend API
- Streamlit frontend interface
- Dockerized deployment

---

## Feature Engineering

Feature engineering was used extensively to make the model more behavior-aware and business-oriented.

The project includes engineered features from multiple perspectives:

### Customer Lifecycle Features

- `Is_New_Customer`
- `Is_Early_Customer`
- `Is_Long_Term`

### Contract Features

- `Is_Month_to_Month`
- `Has_Long_Contract`

### Pricing Features

- `High_Monthly_Charge`
- `Very_High_Monthly_Charge`

### Service Features

- `Has_Fiber`
- `No_Internet`
- `Has_TechSupport`
- `Has_OnlineSecurity`
- `Has_OnlineBackup`
- `Has_DeviceProtection`

### Payment Features

- `Uses_Electronic_Check`
- `Uses_AutoPay`

### Engagement Features

- `Service_Count`
- `Engagement_Score`

### Interaction Features

- `New_Monthly_HighCharge`
- `Fiber_HighCharge`
- `NoSupport_Monthly`
- `ElectronicCheck_Monthly`
- `LowEngagement_HighCharge`
- `Avg_Charge_Per_Tenure`

These engineered features help the model learn customer behavior patterns more effectively compared to using only raw dataset features.

## Static Dataset Limitation

The dataset used in this project is a static snapshot dataset, meaning each customer is represented by a single row at one specific point in time.

While this type of dataset is useful for learning, experimentation, and prototyping, real-world telecom churn prediction systems typically rely on dynamic and time-based behavioral data.

In a real telecom environment, churn prediction models would use continuously updated customer activity data such as:

- Recharge trends
- Data usage trends
- Complaint history
- Customer support interactions
- Network experience and service quality
- Payment delays
- App usage behavior
- Customer engagement patterns

These time-series behavioral signals help telecom companies detect gradual changes in customer engagement and identify early churn indicators more effectively.

This project acknowledges that limitation and uses feature engineering to simulate more behavior-aware customer analysis. However, a production-grade telecom retention system would require continuous customer behavior tracking, real-time data pipelines, and dynamic model updates.

---

## System Architecture

```text
Customer Input
     ↓
Streamlit User Interface
     ↓
FastAPI Backend
     ↓
Feature Engineering
     ↓
XGBoost Churn Prediction
     ↓
K-Means Customer Segmentation
     ↓
Retention Recommendation Logic
     ↓
Prediction Result in UI


