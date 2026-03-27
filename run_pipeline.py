from lambda_app.snowflake_io import read_customer_features, write_predictions
from lambda_app.inference import predict

records = read_customer_features()
results = predict(records)
write_predictions(results)

print("Predictions written to Snowflake successfully.")
print(results)