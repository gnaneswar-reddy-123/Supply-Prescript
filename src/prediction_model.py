import pandas as pd
import joblib

from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report


# Load dataset
data_file = "data/supply_chain_data.csv"

df = pd.read_csv(data_file)

print("Dataset loaded successfully!")
print(f"Rows: {len(df)}")
print(f"Columns: {len(df.columns)}")


# Input features
features = [
    "supplier_reliability",
    "distance_km",
    "order_quantity",
    "inventory_level",
    "transportation_cost",
    "weather_risk",
    "supplier_capacity",
    "demand_level",
    "historical_delay_days"
]

X = df[features]

# Target
y = df["delayed"]


# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("\nTraining records:", len(X_train))
print("Testing records:", len(X_test))


# Create XGBoost model
model = XGBClassifier(
    n_estimators=100,
    max_depth=4,
    learning_rate=0.1,
    random_state=42,
    eval_metric="logloss"
)


# Train model
print("\nTraining XGBoost model...")

model.fit(X_train, y_train)

print("Model training completed!")


# Predictions
y_pred = model.predict(X_test)
y_probability = model.predict_proba(X_test)[:, 1]


# Evaluation
accuracy = accuracy_score(y_test, y_pred)

print("\n--------------------------------")
print("MODEL RESULTS")
print("--------------------------------")

print(f"Accuracy: {accuracy:.2%}")

print("\nClassification Report:")
print(classification_report(y_test, y_pred))


# Save results
results = X_test.copy()

results["actual_delayed"] = y_test.values
results["predicted_delayed"] = y_pred
results["delay_probability"] = y_probability

output_file = "outputs/model_results.csv"

results.to_csv(output_file, index=False)
model_file = "outputs/xgboost_model.pkl"
joblib.dump(model, model_file)

print(f"XGBoost model saved to: {model_file}")

print("--------------------------------")
print(f"Prediction results saved to: {output_file}")
print("--------------------------------")