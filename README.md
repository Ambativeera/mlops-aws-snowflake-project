\# Serverless MLOps Inference Pipeline with AWS Lambda, S3, and Snowflake



\## Project Overview

This project demonstrates how to operationalize a trained machine learning model in a production-style cloud workflow. A churn prediction model is trained locally, exported into a lightweight model configuration, stored in Amazon S3, and used by an AWS Lambda function for inference. Snowflake is used as the data platform for storing input customer records and prediction outputs.



\## Architecture

\- Local training script creates model artifact

\- Model config is stored in Amazon S3

\- AWS Lambda downloads model config from S3 and performs inference

\- Python batch pipeline reads customer features from Snowflake

\- Prediction results are written back to Snowflake



\## Tech Stack

\- Python

\- AWS Lambda

\- Amazon S3

\- IAM

\- Snowflake

\- scikit-learn

\- boto3

\- snowflake-connector-python



\## Project Workflow

1\. Train model locally

2\. Export lightweight model config

3\. Upload model config to S3

4\. Deploy Lambda inference function

5\. Read customer features from Snowflake

6\. Generate predictions

7\. Write predictions back to Snowflake



\## Key Features

\- Serverless inference with AWS Lambda

\- Model artifact storage in Amazon S3

\- Snowflake integration for batch input and output

\- IAM-based secure access control

\- Lightweight deployment approach for reduced Lambda package size



\## Files

\- `model/train\_model.py` - trains the original churn model

\- `model/export\_model\_config.py` - exports lightweight model config

\- `model/model\_config.json` - lightweight model artifact used by Lambda

\- `lambda\_app/inference.py` - loads model config and performs predictions

\- `lambda\_app/handler.py` - Lambda entry point

\- `lambda\_app/snowflake\_io.py` - reads and writes Snowflake data

\- `run\_pipeline.py` - runs Snowflake batch inference locally

\- `test\_local.py` - tests inference locally



\## Known Limitation

Direct Snowflake connectivity inside AWS Lambda was not finalized in this version because the Snowflake connector package built on Windows was not compatible with the Linux Lambda runtime. To keep the deployment lightweight and functional, Snowflake integration is handled through a Python batch pipeline outside Lambda.



\## Outcome

This project demonstrates a production-focused MLOps pattern where model artifacts are managed in S3, inference is deployed in AWS Lambda, and Snowflake is used for batch feature input and prediction output.

