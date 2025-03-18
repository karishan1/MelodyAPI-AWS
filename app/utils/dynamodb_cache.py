from fastapi import FastAPI, HTTPException
import boto3
import time, json, subprocess
from pydantic import BaseModel
from decimal import Decimal

app = FastAPI()

dynamodb = boto3.resource(
    "dynamodb",
    region_name="us-west-2",
    endpoint_url="http://localhost:8000"
)

table_name = "AudioCache"

def create_table():
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
    """ Recursively converts floats in a dictionary or list to Decimal """
    if isinstance(data, float):
        return Decimal(str(data))
    elif isinstance(data, list):
        return [convert_floats_to_decimal(x) for x in data]
    elif isinstance(data, dict):
        return {k: convert_floats_to_decimal(v) for k, v in data.items()}
    return data

def store_fingerprint(audio_fingerprint, classification):
    if check_if_fingerprint_exists(audio_fingerprint):
        return {"message": "Fingerprint Already Exists in DB"}

    try:
        classification = convert_floats_to_decimal(classification)

        table = dynamodb.Table("AudioCache")
        table.put_item(
            Item={
                "fingerprint": audio_fingerprint,
                "classification": classification,
                "timestamp": int(time.time())
            }
        )
        return {"message": "Fingerprint Stored Successfully"}
    except Exception as e:
        return {"error": str(e)}

def get_fingerprint(fingerprint :str):
    try:
        table = dynamodb.Table("AudioCache")
        response = table.get_item(Key = {"fingerprint" : fingerprint})
        item = response.get("Item")
        return item
    except Exception as e :
        return {"error": str(e)}
    
def check_if_fingerprint_exists(fingerprint : str):
    table = dynamodb.Table("AudioCache")
    response = table.get_item(Key = {"fingerprint" : fingerprint})
    if "Item" in response:
        return True
    return False

def generate_fingerprint(audio_file):
    
    try:
        result = subprocess.run(["fpcalc","-json",audio_file], capture_output=True, text=True)
        fingerprint_data = json.loads(result.stdout)
        return fingerprint_data.get("fingerprint")
    except Exception as e:
        print(f"Error generating fingerprint: {e}")
        return None
