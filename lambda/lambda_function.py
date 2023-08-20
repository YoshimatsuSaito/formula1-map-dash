import io
import os
import pickle
import sys
from datetime import datetime
from io import BytesIO

import boto3
import pandas as pd

from preprocessing_pipeline import (
    retrieve_data_for_inference,
    transform_data,
    generate_features,
    LIST_COL_X,
    LIST_COL_y,
    LIST_COL_IDENTIFIER,
)

BUCKET_NAME = os.environ.get("BUCKET_NAME")
CURRENT_SEASON = 2023
current_date = datetime.now().strftime("%y%m%d")


def lambda_handler(event, context):
    df = retrieve_data_for_inference(CURRENT_SEASON)
    df = transform_data(df)
    df = generate_features(df)

    s3 = boto3.client("s3")
    csv_buffer = BytesIO()
    df.to_csv(csv_buffer, index=False)
    s3.put_object(
        Bucket=BUCKET_NAME,
        Key=f"features/features_{current_date}.csv",
        Body=csv_buffer.getvalue(),
    )
