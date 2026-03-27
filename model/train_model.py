import json
import os
import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression

data = pd.DataFrame([
    {"customer_id": 1, "tenure": 2, "monthly_charges": 95, "contract_type": "Month-to-month", "support_tickets": 4, "churn": 1},
    {"customer_id": 2, "tenure": 24, "monthly_charges": 45, "contract_type": "One year", "support_tickets": 1, "churn": 0},
    {"customer_id": 3, "tenure": 1, "monthly_charges": 110, "contract_type": "Month-to-month", "support_tickets": 5, "churn": 1},
    {"customer_id": 4, "tenure": 36, "monthly_charges": 60, "contract_type": "Two year", "support_tickets": 0, "churn": 0},
    {"customer_id": 5, "tenure": 8, "monthly_charges": 85, "contract_type": "Month-to-month", "support_tickets": 3, "churn": 1},
    {"customer_id": 6, "tenure": 18, "monthly_charges": 55, "contract_type": "One year", "support_tickets": 1, "churn": 0},
])

X = data[["tenure", "monthly_charges", "contract_type", "support_tickets"]]
y = data["churn"]

numeric_features = ["tenure", "monthly_charges", "support_tickets"]
categorical_features = ["contract_type"]

numeric_transformer = Pipeline(steps=[
    ("imputer", SimpleImputer(strategy="median"))
])

categorical_transformer = Pipeline(steps=[
    ("imputer", SimpleImputer(strategy="most_frequent")),
    ("onehot", OneHotEncoder(handle_unknown="ignore"))
])

preprocessor = ColumnTransformer(
    transformers=[
        ("num", numeric_transformer, numeric_features),
        ("cat", categorical_transformer, categorical_features),
    ]
)

model = Pipeline(steps=[
    ("preprocessor", preprocessor),
    ("classifier", LogisticRegression())
])

model.fit(X, y)

os.makedirs("model", exist_ok=True)
joblib.dump(model, "model/model.pkl")

with open("model/feature_columns.json", "w") as f:
    json.dump(["tenure", "monthly_charges", "contract_type", "support_tickets"], f)

print("Model saved successfully.")