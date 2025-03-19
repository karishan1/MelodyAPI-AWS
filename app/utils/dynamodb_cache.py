from fastapi import FastAPI, HTTPException
import boto3
import time, json, subprocess
from pydantic import BaseModel
from decimal import Decimal

app = FastAPI()

dynamodb = boto3.resource(
    "dynamodb",
    region_name="eu-west-2",
    endpoint_url="http://localhost:8000"
)

table_name = "Audio-Cache"

def create_table():
    table_name = "Audio-Cache"
    try:
        existing_tables = dynamodb.meta.client.list_tables()["TableNames"]
        if table_name not in existing_tables:
            table = dynamodb.create_table(
                TableName=table_name,
                KeySchema=[{"AttributeName": "fingerprint", "KeyType": "HASH"}],
                AttributeDefinitions=[{"AttributeName": "fingerprint", "AttributeType": "S"}],
                ProvisionedThroughput={"ReadCapacityUnits": 5, "WriteCapacityUnits": 5},
            )
            table.wait_until_exists()
            print("Table created successfully!")
    except Exception as e:
        print(f"Error creating table: {e}")

def init_db():
    create_table()

def convert_floats_to_decimal(data):
    if isinstance(data, float):
        return Decimal(str(data))
    elif isinstance(data, list):
        return [convert_floats_to_decimal(x) for x in data]
    elif isinstance(data, dict):
        return {k: convert_floats_to_decimal(v) for k, v in data.items()}
    return data

def store_fingerprint(fingerprint, category, classification, predictions_num=None):

    try:
        if predictions_num:
            cache_key = f"{fingerprint}_{category}_{predictions_num}"
        else:
            cache_key = f"{fingerprint}_{category}"
        classification = convert_floats_to_decimal(classification)

        table = dynamodb.Table("Audio-Cache")
        table.put_item(
            Item={
                "fingerprint": cache_key,
                "category": category,
                "predictions_num": predictions_num if predictions_num else 0,
                "classification": classification,
            }
        )
        return {"message": "Fingerprint Stored Successfully"}
    except Exception as e:
        return {"error": str(e)}

def get_fingerprint(fingerprint :str, category : str, predictions_num = None):
    try:

        if predictions_num:
            cache_key = f"{fingerprint}_{category}_{predictions_num}"
        else:
            cache_key = f"{fingerprint}_{category}"

        table = dynamodb.Table("Audio-Cache")
        response = table.get_item(Key = {"fingerprint" : cache_key})
        item = response.get("Item")
        return item
    except Exception as e :
        return {"error": str(e)}
    


def generate_fingerprint(audio_file):
    
    try:
        result = subprocess.run(["fpcalc","-json",audio_file], capture_output=True, text=True)
        fingerprint_data = json.loads(result.stdout)
        return fingerprint_data.get("fingerprint")
    except Exception as e:
        print(f"Error generating fingerprint: {e}")
        return None
