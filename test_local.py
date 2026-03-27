from lambda_app.handler import lambda_handler

event = {
    "records": [
        {
            "customer_id": 101,
            "tenure": 3,
            "monthly_charges": 99,
            "contract_type": "Month-to-month",
            "support_tickets": 4
        },
        {
            "customer_id": 102,
            "tenure": 30,
            "monthly_charges": 50,
            "contract_type": "Two year",
            "support_tickets": 0
        }
    ]
}

response = lambda_handler(event, None)
print(response)