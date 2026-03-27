import json
import math
import os
import tempfile
import boto3

BUCKET_NAME = os.getenv("MODEL_BUCKET")
MODEL_CONFIG_KEY = "model_config.json"

TEMP_DIR = tempfile.gettempdir()
LOCAL_CONFIG_PATH = os.path.join(TEMP_DIR, "model_config.json")

s3 = boto3.client("s3")


def download_file_from_s3(bucket_name, s3_key, local_path):
    s3.download_file(bucket_name, s3_key, local_path)


def load_model_config():
    if BUCKET_NAME:
        download_file_from_s3(BUCKET_NAME, MODEL_CONFIG_KEY, LOCAL_CONFIG_PATH)
        with open(LOCAL_CONFIG_PATH, "r") as f:
            return json.load(f)
    with open("model/model_config.json", "r") as f:
        return json.load(f)


def sigmoid(x):
    return 1 / (1 + math.exp(-x))


def build_feature_vector(record, feature_names):
    vector = []

    for feature in feature_names:
        if feature == "num__tenure":
            vector.append(float(record.get("tenure", 0)))
        elif feature == "num__monthly_charges":
            vector.append(float(record.get("monthly_charges", 0)))
        elif feature == "num__support_tickets":
            vector.append(float(record.get("support_tickets", 0)))
        elif feature == "cat__contract_type_Month-to-month":
            vector.append(1.0 if record.get("contract_type") == "Month-to-month" else 0.0)
        elif feature == "cat__contract_type_One year":
            vector.append(1.0 if record.get("contract_type") == "One year" else 0.0)
        elif feature == "cat__contract_type_Two year":
            vector.append(1.0 if record.get("contract_type") == "Two year" else 0.0)
        else:
            vector.append(0.0)

    return vector


def predict(records):
    config = load_model_config()
    feature_names = config["feature_names"]
    coefficients = config["coefficients"]
    intercept = config["intercept"]
    model_version = config.get("model_version", "v1")

    results = []

    for record in records:
        feature_vector = build_feature_vector(record, feature_names)
        score = intercept + sum(c * x for c, x in zip(coefficients, feature_vector))
        probability = sigmoid(score)
        prediction = 1 if probability >= 0.5 else 0

        results.append({
            "customer_id": record["customer_id"],
            "prediction": prediction,
            "probability": probability,
            "model_version": model_version
        })

    return results