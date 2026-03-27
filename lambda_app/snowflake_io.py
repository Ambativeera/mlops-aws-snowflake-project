import os
import snowflake.connector
from datetime import datetime

def get_connection():
    return snowflake.connector.connect(
        user=os.getenv("SNOWFLAKE_USER"),
        password=os.getenv("SNOWFLAKE_PASSWORD"),
        account=os.getenv("SNOWFLAKE_ACCOUNT"),
        warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
        database=os.getenv("SNOWFLAKE_DATABASE"),
        schema=os.getenv("SNOWFLAKE_SCHEMA")
    )

def read_customer_features():
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            SELECT customer_id, tenure, monthly_charges, contract_type, support_tickets
            FROM customer_features
        """)
        rows = cur.fetchall()
        return [
            {
                "customer_id": row[0],
                "tenure": row[1],
                "monthly_charges": row[2],
                "contract_type": row[3],
                "support_tickets": row[4]
            }
            for row in rows
        ]
    finally:
        cur.close()
        conn.close()

def write_predictions(results):
    conn = get_connection()
    cur = conn.cursor()
    try:
        for row in results:
            cur.execute("""
                INSERT INTO customer_predictions
                (customer_id, prediction, probability, model_version, inference_timestamp)
                VALUES (%s, %s, %s, %s, %s)
            """, (
                row["customer_id"],
                row["prediction"],
                row["probability"],
                row["model_version"],
                datetime.utcnow()
            ))
        conn.commit()
    finally:
        cur.close()
        conn.close()