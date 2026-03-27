import json
from inference import predict
from snowflake_io import read_customer_features, write_predictions

def lambda_handler(event, context):
    records = event.get("records")

    if not records:
        records = read_customer_features()
        results = predict(records)
        write_predictions(results)

        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "Predictions read from Snowflake and written back successfully.",
                "rows_processed": len(results),
                "results": results
            })
        }

    results = predict(records)

    return {
        "statusCode": 200,
        "body": json.dumps(results)
    }