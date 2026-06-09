# Contributing to SentinelIQ

Thank you for your interest in contributing to SentinelIQ. This guide covers everything you need to get started — from understanding the architecture to submitting your first pull request.

---

## Table of Contents

- [Project Architecture](#project-architecture)
- [Setup Instructions](#setup-instructions)
- [Contribution Workflow](#contribution-workflow)
- [Coding Standards](#coding-standards)

---

## Project Architecture

SentinelIQ is a full-stack fraud detection platform with three main layers: a Python/FastAPI backend, a React frontend, and a machine learning pipeline.

### Repository Layout

```text
SentinelIQ/
├── main.py             # FastAPI application — all API routes
├── train_model.py      # ML training script (run once to generate .pkl files)
├── requirements.txt    # Python dependencies
├── fraud_model.pkl     # Trained Random Forest model (generated, not committed)
├── anomaly_model.pkl   # Trained Isolation Forest model (generated, not committed)
│
├── src/                # React frontend source
│   ├── main.jsx        # React entry point
│   └── App.jsx         # Root component and routing
│
├── index.html          # HTML shell for Vite/React
├── package.json        # Node dependencies and scripts
├── vite.config.js      # Vite + Tailwind build config
└── eslint.config.js    # ESLint rules
```

### Backend (FastAPI)

`main.py` is the single-file backend. On startup it loads two pre-trained models from disk using `joblib`:

| Model | File | Purpose |
|---|---|---|
| Random Forest Classifier | `fraud_model.pkl` | Classifies a transaction as fraud or legitimate |
| Isolation Forest | `anomaly_model.pkl` | Flags statistically anomalous transactions |

**API Endpoints**

| Method | Route | Description |
|---|---|---|
| `GET` | `/` | Health check, returns required feature list |
| `POST` | `/predict` | Scores a single transaction |
| `POST` | `/batch-predict` | Accepts a CSV file, returns batch results |

The `/predict` endpoint accepts a JSON body with 30 features (`Time`, `V1`–`V28`, `Amount`) — matching the [Kaggle Credit Card Fraud dataset](https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud) schema — and returns:

```json
{
  "fraud_prediction": 0,
  "fraud_probability": 0.043,
  "anomaly_detected": false,
  "risk_level": "LOW"
}
```

Risk level thresholds: `fraud_probability > 0.75` → HIGH, `> 0.40` → MEDIUM, otherwise LOW.

### Machine Learning Pipeline

`train_model.py` trains both models from `../dataset/creditcard.csv`:

1. Load the raw credit card dataset (highly imbalanced — ~0.17% fraud).
2. Apply **SMOTE** (Synthetic Minority Oversampling) to balance the classes.
3. Train a **Random Forest Classifier** (120 estimators) on the balanced dataset.
4. Train an **Isolation Forest** (contamination=0.01) on the same training split.
5. Serialize both models to `fraud_model.pkl` and `anomaly_model.pkl` via `joblib`.

> `train_model.py` requires `imbalanced-learn` in addition to `requirements.txt`. Install it with `pip install imbalanced-learn` before running.

### Frontend (React + Vite)

The frontend is built with React 19, Vite, TailwindCSS 4, and Recharts. It calls the FastAPI backend at `http://localhost:8000` using Axios.

Key libraries:

| Library | Purpose |
|---|---|
| `recharts` | Charts and data visualizations |
| `axios` | HTTP requests to the backend API |
| `lucide-react` | Icon set |
| `tailwindcss` | Utility-first CSS |

### Data Flow

```
User Input / CSV Upload
        │
        ▼
  React Frontend  ──── POST /predict ────▶  FastAPI Backend
        │                                         │
        │                                  Random Forest
        │                                  Isolation Forest
        │                                         │
        ◀──────── JSON Response ─────────────────
        │
  Recharts Dashboard
```

---

## Setup Instructions

### Prerequisites

- **Python** 3.9 or higher
- **Node.js** 18 or higher and **npm**
- The [Credit Card Fraud Detection dataset](https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud) CSV placed at `../dataset/creditcard.csv` relative to the repo root (only needed if you plan to retrain the models)

### 1. Clone the Repository

```bash
git clone https://github.com/krishnaprasharkp/SentinelIQ.git
cd SentinelIQ
```

### 2. Backend Setup

Create and activate a virtual environment, then install dependencies:

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

pip install -r requirements.txt
```

#### Train the Models (first-time only)

If pre-trained `.pkl` files are not present in the repo root, you must generate them:

```bash
pip install imbalanced-learn     # extra dependency for SMOTE
python train_model.py
```

This produces `fraud_model.pkl` and `anomaly_model.pkl` in the current directory.

#### Start the Backend Server

```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`. Visit `http://localhost:8000/docs` for the auto-generated Swagger UI.

### 3. Frontend Setup

In a separate terminal from the repo root:

```bash
npm install
npm run dev
```

The React app will be available at `http://localhost:5173`.

### 4. Verify the Setup

With both servers running, the frontend at `http://localhost:5173` should connect to the backend automatically. You can also test the API directly:

```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"Time": 100, "V1": 1.2, "V2": -0.5, "V3": 0, "V4": 0, "V5": 0, "V6": 0, "V7": 0, "V8": 0, "V9": 0, "V10": 0, "V11": 0, "V12": 0, "V13": 0, "V14": 0, "V15": 0, "V16": 0, "V17": 0, "V18": 0, "V19": 0, "V20": 0, "V21": 0, "V22": 0, "V23": 0, "V24": 0, "V25": 0, "V26": 0, "V27": 0, "V28": 0, "Amount": 250.00}'
```

---

## Contribution Workflow

### 1. Fork and Branch

Fork the repository on GitHub, then create a branch for your change:

```bash
git checkout -b <type>/<short-description>
```

Branch naming conventions:

| Prefix | Use for |
|---|---|
| `feature/` | New functionality |
| `fix/` | Bug fixes |
| `docs/` | Documentation only |
| `refactor/` | Code restructuring without behavior change |
| `test/` | Adding or improving tests |

Examples: `feature/dark-mode`, `fix/batch-predict-csv-error`, `docs/api-examples`

### 2. Make Your Changes

Keep each pull request focused on a single concern. If you discover an unrelated bug while working, open a separate issue or PR for it.

### 3. Test Your Changes

- **Backend:** Verify the API endpoints still respond correctly with `curl` or the Swagger UI at `/docs`.
- **Frontend:** Run `npm run lint` and confirm the UI behaves correctly in a browser.
- **Models:** If you modify `train_model.py`, re-run it and confirm the classification report looks reasonable before committing new `.pkl` files.

### 4. Commit

Write clear, present-tense commit messages that explain *what* and *why*:

```bash
# Good
git commit -m "Add risk trend chart to dashboard"
git commit -m "Fix batch-predict crash when CSV has missing columns"

# Avoid
git commit -m "fix stuff"
git commit -m "WIP"
```

### 5. Open a Pull Request

Push your branch and open a PR against `main`. Fill in the PR template — include a short summary, what you tested, and screenshots for any UI changes. A maintainer will review and may request changes before merging.

---

## Coding Standards

### Python (Backend)

- Follow [PEP 8](https://peps.python.org/pep-0008/) style guidelines.
- Use type hints on function signatures where practical.
- Keep route handlers thin — business logic belongs in helper functions, not inline in the endpoint.
- Do not commit `.pkl` model files that were trained on private data; only commit models trained on the public Kaggle dataset.
- Format with `black` if possible: `pip install black && black main.py train_model.py`

**Example — preferred endpoint style:**

```python
@app.post("/predict")
def predict_fraud(transaction: Transaction):
    data = pd.DataFrame([transaction.dict()], columns=feature_names)
    fraud_prediction = fraud_model.predict(data)[0]
    fraud_probability = fraud_model.predict_proba(data)[0][1]
    anomaly_prediction = anomaly_model.predict(data)[0]
    return build_prediction_response(fraud_prediction, fraud_probability, anomaly_prediction)
```

### JavaScript / React (Frontend)

- Use **functional components** with hooks only — no class components.
- One component per file; file name matches the component name (PascalCase).
- Keep components small. If a component exceeds ~100 lines, consider splitting it.
- Use `axios` for all HTTP calls; do not use `fetch` directly.
- Run the linter before committing: `npm run lint`

**Component naming:**

```
src/
├── components/
│   ├── RiskScoreCard.jsx     ✓ PascalCase, matches component name
│   └── TransactionTable.jsx
└── pages/
    ├── Dashboard.jsx
    └── BatchUpload.jsx
```

### General

- Do not commit secrets, API keys, or private datasets.
- Update the README if you add a new endpoint, environment variable, or setup step.
- Prefer clarity over brevity — readable code is more valuable than clever one-liners.

---

## Areas Where Contributions Are Especially Welcome

- Unit and integration tests (there are none yet — this is a great first issue!)
- Docker / `docker-compose` setup
- Explainable AI with SHAP values
- Dark mode for the dashboard
- User authentication (JWT)
- Improved model evaluation metrics and visualizations
- Cloud deployment guide (Render, Railway, Fly.io, etc.)

---

## Questions?

Open an issue with the `question` label or start a GitHub Discussion. We are happy to help first-time contributors get oriented.
