import json
import joblib

model = joblib.load("model/model.pkl")

preprocessor = model.named_steps["preprocessor"]
classifier = model.named_steps["classifier"]

feature_names = preprocessor.get_feature_names_out().tolist()
coefficients = classifier.coef_[0].tolist()
intercept = float(classifier.intercept_[0])

config = {
    "feature_names": feature_names,
    "coefficients": coefficients,
    "intercept": intercept,
    "model_version": "v1"
}

with open("model/model_config.json", "w") as f:
    json.dump(config, f, indent=2)

print("model_config.json created successfully.")