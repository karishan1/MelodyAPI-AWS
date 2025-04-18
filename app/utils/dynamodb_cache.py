from fastapi import FastAPI, HTTPException
import boto3
import time, json, subprocess
from pydantic import BaseModel
from decimal import Decimal

# Initialize FastAPI application
app = FastAPI()

# Connect to DynamoDB instance
dynamodb = boto3.resource(
    "dynamodb",
    region_name="eu-west-2",
    endpoint_url="http://localhost:8000" # Endpoint
)

# Name of the DynamoDB table for caching
table_name = "Audio-Cache"

# Initialize the database
def init_db():
    create_table()

# Create the DynamoDB table if it doesn't exist
def create_table():
    table_name = "Audio-Cache"
    try:
        # Get list of existing tables
        existing_tables = dynamodb.meta.client.list_tables()["TableNames"]

        # Only create the table if it doesn't exist
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

# Recursively converts float values to Decimal
def convert_floats_to_decimal(data):
    if isinstance(data, float):
        return Decimal(str(data))
    elif isinstance(data, list):
        return [convert_floats_to_decimal(x) for x in data]
    elif isinstance(data, dict):
        return {k: convert_floats_to_decimal(v) for k, v in data.items()}
    return data

# Stores a fingerprint and corresponding classification results in DynamoDB
def store_fingerprint(fingerprint, category, classification, predictions_num=None,ttl_seconds=86400):

    try:
        if predictions_num:
            cache_key = f"{fingerprint}_{category}_{predictions_num}"
        else:
            cache_key = f"{fingerprint}_{category}"

        # Ensures all float values are converted to decimal format
        classification = convert_floats_to_decimal(classification)
        timestamp = int(time.time())
        expire_at = timestamp + ttl_seconds

        # Puts item into DynamoDB
        table = dynamodb.Table("Audio-Cache")
        table.put_item(
            Item={
                "fingerprint": cache_key,
                "category": category,
                "predictions_num": predictions_num if predictions_num else 0,
                "classification": classification,
                "ttl": expire_at,
            }
        )
        return {"message": "Fingerprint Stored Successfully"}
    except Exception as e:
        return {"error": str(e)}

# Retrieves cached result for specific query
def get_fingerprint(fingerprint :str, category : str, predictions_num = None):
    try:
        # Changes cache key depending on category and number of results wanted
        if predictions_num:
            cache_key = f"{fingerprint}_{category}_{predictions_num}"
        else:
            cache_key = f"{fingerprint}_{category}"

        # Queries the DynamoDB table using the key
        table = dynamodb.Table("Audio-Cache")
        response = table.get_item(Key = {"fingerprint" : cache_key})
        item = response.get("Item")
        return item
    except Exception as e :
        return {"error": str(e)}
    

# Generate a unique fingerprint for a given audio file
def generate_fingerprint(audio_file):
    try:
        # Run the fpcalc command with JSON output
        result = subprocess.run(["fpcalc","-json",audio_file], capture_output=True, text=True)
        fingerprint_data = json.loads(result.stdout)
        return fingerprint_data.get("fingerprint")
    except Exception as e:
        print(f"Error generating fingerprint: {e}")
        return None
