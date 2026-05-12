from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import create_model
import pandas as pd
import joblib
import io

app = FastAPI(
    title="SentinelIQ Fraud Detection API",
    description="Real-world AI fraud detection using Random Forest, Isolation Forest, and SMOTE-trained data",
    version="2.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5174"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

fraud_model = joblib.load("fraud_model.pkl")
anomaly_model = joblib.load("anomaly_model.pkl")

feature_names = ["Time"] + [f"V{i}" for i in range(1, 29)] + ["Amount"]

Transaction = create_model(
    "Transaction",
    **{feature: (float, 0.0) for feature in feature_names}
)

@app.get("/")
def home():
    return {
        "message": "SentinelIQ Real Fraud Detection API Running",
        "features_required": feature_names
    }

@app.post("/predict")
def predict_fraud(transaction: Transaction):
    input_dict = transaction.dict()
    data = pd.DataFrame([input_dict], columns=feature_names)

    fraud_prediction = fraud_model.predict(data)[0]
    fraud_probability = fraud_model.predict_proba(data)[0][1]
    anomaly_prediction = anomaly_model.predict(data)[0]

    risk_level = "LOW"
    if fraud_probability > 0.75:
        risk_level = "HIGH"
    elif fraud_probability > 0.40:
        risk_level = "MEDIUM"

    return {
        "fraud_prediction": int(fraud_prediction),
        "fraud_probability": round(float(fraud_probability), 4),
        "anomaly_detected": bool(anomaly_prediction == -1),
        "risk_level": risk_level,
        "message": "Real fraud detection completed successfully"
    }

@app.post("/batch-predict")
async def batch_predict(file: UploadFile = File(...)):
    contents = await file.read()
    df = pd.read_csv(io.BytesIO(contents))

    missing_cols = [col for col in feature_names if col not in df.columns]

    if missing_cols:
        return {
            "error": "CSV missing required columns",
            "missing_columns": missing_cols
        }

    data = df[feature_names]

    predictions = fraud_model.predict(data)
    probabilities = fraud_model.predict_proba(data)[:, 1]
    anomalies = anomaly_model.predict(data)

    df["fraud_prediction"] = predictions
    df["fraud_probability"] = probabilities.round(4)
    df["anomaly_detected"] = anomalies == -1

    def risk(prob):
        if prob > 0.75:
            return "HIGH"
        elif prob > 0.40:
            return "MEDIUM"
        return "LOW"

    df["risk_level"] = df["fraud_probability"].apply(risk)

    total_transactions = len(df)
    fraud_count = int(df["fraud_prediction"].sum())
    high_risk_count = int((df["risk_level"] == "HIGH").sum())

    return {
        "total_transactions": total_transactions,
        "fraud_count": fraud_count,
        "safe_count": total_transactions - fraud_count,
        "high_risk_count": high_risk_count,
        "fraud_rate": round((fraud_count / total_transactions) * 100, 2),
        "sample_results": df.head(10).to_dict(orient="records")
    }