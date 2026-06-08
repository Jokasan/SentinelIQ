# SentinelIQ

Machine Learning-Powered Fraud Detection and Risk Analytics Platform

SentinelIQ is a full-stack fraud detection platform that combines supervised and unsupervised machine learning techniques to identify fraudulent transactions, detect anomalies, and provide actionable risk insights through an interactive analytics dashboard.

The platform is designed to assist analysts, researchers, and developers in monitoring transaction behavior and evaluating financial risks using data-driven approaches.

---

## Key Features

- Fraud Detection using Random Forest Classification
- Anomaly Detection using Isolation Forest
- Real-Time Risk Assessment
- Batch Transaction Analysis via CSV Upload
- Interactive Analytics Dashboard
- REST API Integration with FastAPI
- Transaction Risk Scoring and Monitoring
- Data Visualization and Reporting

---

## Problem Statement

Financial fraud remains a critical challenge across banking, fintech, and e-commerce systems. Traditional rule-based systems often struggle to identify sophisticated fraudulent activities and evolving attack patterns.

SentinelIQ addresses this challenge by combining machine learning-based classification and anomaly detection techniques to identify suspicious transactions and generate risk insights for decision-making.

---

## System Architecture

```text
Transaction Dataset
        │
        ▼
Data Preprocessing
        │
        ▼
Random Forest Classifier
        │
        ▼
Fraud Prediction
        │
        ▼
Isolation Forest
        │
        ▼
Anomaly Detection
        │
        ▼
Risk Analytics Dashboard
```

## Technology Stack

### Backend

- Python
- FastAPI
- Scikit-Learn
- Pandas
- NumPy

### Frontend

- React
- Vite
- Recharts

### Machine Learning

- Random Forest Classifier
- Isolation Forest

### Dataset

- Credit Card Fraud Detection Dataset

---

## Project Structure

```text
SentinelIQ
│
├── backend
│   ├── models
│   ├── routes
│   ├── app.py
│   └── requirements.txt
│
├── frontend
│   ├── src
│   ├── components
│   └── pages
│
├── screenshots
│
└── README.md
```

## Installation

### Clone the Repository

```bash
git clone https://github.com/krishnaprasharkp/SentinelIQ.git

cd SentinelIQ
```

### Backend Setup

```bash
cd backend

pip install -r requirements.txt

uvicorn app:app --reload
```

Backend runs at:

```text
http://localhost:8000
```

### Frontend Setup

```bash
cd frontend

npm install

npm run dev
```

Frontend runs at:

```text
http://localhost:5173
```

---

## API Endpoint

### Predict Transaction Risk

**POST** `/predict`

Example Request:

```json
{
  "Time": 100,
  "Amount": 250.00,
  "V1": 1.2,
  "V2": -0.5
}
```

Example Response:

```json
{
  "fraud_prediction": 0,
  "risk_score": 0.08,
  "anomaly_flag": false
}
```

---

## Dashboard Insights

The dashboard provides:

- Fraud Prediction Results
- Transaction Risk Scores
- Anomaly Detection Analysis
- Transaction Distribution Metrics
- Risk Trend Visualization
- High-Risk Transaction Monitoring

---

## Future Enhancements

- User Authentication
- Explainable AI using SHAP
- Docker Support
- Cloud Deployment
- Real-Time Streaming Analysis
- Alert Notification System
- Model Retraining Pipeline
- Role-Based Access Control

---

## Contributing

Contributions are welcome.

1. Fork the repository
2. Create a new feature branch

```bash
git checkout -b feature/new-feature
```

3. Commit your changes

```bash
git commit -m "Add new feature"
```

4. Push the branch

```bash
git push origin feature/new-feature
```

5. Open a Pull Request

---

## License

This project is licensed under the MIT License.

---

## Author

Krishna Prashar

B.Tech Computer Science Engineering  
Guru Nanak Dev University, Amritsar

GitHub: https://github.com/krishnaprasharkp
