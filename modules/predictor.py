import os
import pickle
import sys
from io import BytesIO

import boto3
import pandas as pd
from dotenv import load_dotenv
from lightgbm import LGBMClassifier

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(os.path.dirname(current_dir), "modules"))

from preprocessing_pipeline import LIST_COL_X

load_dotenv(".env")
AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
BUCKET_NAME = os.environ.get("BUCKET_NAME")


class Predictor:
    """Load pretrained model and features and predict grandprix result"""
    def __init__(self):
        self.s3 = boto3.client(
            "s3",
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        )
        self._load_model()
        self._load_features()

    def _load_model(self):
        """Load a pretrained model"""
        obj = self.s3.get_object(Bucket=BUCKET_NAME, Key="model.pkl")
        body = obj['Body'].read()
        self.model = pickle.loads(body)    
    
    def _load_features(self):
        """Load features created most recently"""
        objs = self.s3.list_objects_v2(Bucket=BUCKET_NAME, Prefix='features/features_')
        latest_obj_key = sorted(objs.get('Contents', []), key=lambda x: x['LastModified'], reverse=True)[0]["Key"]
        
        obj = self.s3.get_object(Bucket=BUCKET_NAME, Key=f"{latest_obj_key}")
        self.df = pd.read_csv(obj['Body'])
        
    def predict(self):
        """Predict"""
        y_pred = self.model.predict_proba(self.df.loc[:, LIST_COL_X])[:, 1]
        self.df["pred"] = y_pred
        return self.df
