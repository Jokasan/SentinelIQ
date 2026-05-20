import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, IsolationForest
from sklearn.metrics import classification_report, accuracy_score

from imblearn.over_sampling import SMOTE

# Load real fraud dataset
data = pd.read_csv("../dataset/creditcard.csv")

# Features and target
X = data.drop("Class", axis=1)
y = data["Class"]

print("Original Fraud Distribution:")
print(y.value_counts())

# Handle imbalanced fraud data using SMOTE
smote = SMOTE(random_state=42)

X_resampled, y_resampled = smote.fit_resample(X, y)

print("\nBalanced Fraud Distribution:")
print(pd.Series(y_resampled).value_counts())

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X_resampled,
    y_resampled,
    test_size=0.2,
    random_state=42
)

# Fraud classifier model
model = RandomForestClassifier(
    n_estimators=120,
    random_state=42,
    n_jobs=-1
)

model.fit(X_train, y_train)

# Anomaly detection model
anomaly_model = IsolationForest(
    contamination=0.01,
    random_state=42
)

anomaly_model.fit(X_train)

# Predictions
predictions = model.predict(X_test)

print("\nAccuracy:")
print(accuracy_score(y_test, predictions))

print("\nClassification Report:")
print(classification_report(y_test, predictions))

# Save trained models
joblib.dump(model, "fraud_model.pkl")
joblib.dump(anomaly_model, "anomaly_model.pkl")

print("\nReal-world fraud models trained successfully.")
