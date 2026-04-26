import boto3
import json
import time
import random
from datetime import datetime

STREAM_NAME = "suriya-bank-fraud-stream"
REGION = "ap-southeast-1"

kinesis_client = boto3.client('kinesis', region_name=REGION)

def generate_transaction():

    account_pool = ["ACC1001", "ACC1002", "ACC1003", "ACC2001", "ACC2002"]
    
    account_id = random.choice(account_pool)
    amount = round(random.uniform(10.0, 500000.0), 2)
    
    if account_id == "ACC2002" and random.random() > 0.8:
        amount = round(random.uniform(20000.0, 500000.0), 2)

    return {
        "transaction_id": f"TXN{int(time.time()*1000)}",
        "account_id": account_id,
        "amount": amount,
        "currency": "THB",
        "transaction_type": random.choice(["TRANSFER", "PAYMENT", "WITHDRAWAL"]),
        "timestamp": datetime.utcnow().isoformat(),
        "device_id": f"DEV-{random.randint(100, 199)}",
        "location": random.choice(["Bangkok", "Nonthaburi", "Phuket", "Chiang Mai"])
    }

print(f"🚀 Starting Producer for stream: {STREAM_NAME}...")

try:
    while True:
        data = generate_transaction()
        response = kinesis_client.put_record(
            StreamName=STREAM_NAME,
            Data=json.dumps(data),
            PartitionKey=data["account_id"] 
        )
        print(f"✅ Sent: {data['transaction_id']} | Account: {data['account_id']} | Amount: {data['amount']}")
        time.sleep(random.uniform(3.0, 6.0))  
except KeyboardInterrupt:
    print("Stopping Producer...")