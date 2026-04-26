import base64
import json
import os
import boto3
from datetime import datetime

s3 = boto3.client('s3')

def lambda_handler(event, context):
    bucket_name = os.environ['S3_BUCKET']
    now = datetime.now()
    
    partition_path = now.strftime("bronze/year=%Y/month=%m/day=%d/hour=%H")
    
    for record in event['Records']:
        payload = base64.b64decode(record['kinesis']['data']).decode('utf-8')
        data = json.loads(payload)
        
        if not data.get('account_id') or data.get('amount') is None:
            print(f"Skipping record: Missing essential fields in {data}")
            continue
        
        if data['amount'] < 0:
            print(f"Skipping record: Invalid amount {data['amount']}")
            continue
        
        data['risk_fraud'] = True if data.get('amount', 0) > 300000 else False
        data['processed_at'] = now.isoformat()
        
        file_name = f"{partition_path}/transaction_{record['kinesis']['sequenceNumber']}.json"
        
        s3.put_object(
            Bucket=bucket_name,
            Key=file_name,
            Body=json.dumps(data)
        )
        
    return {'statusCode': 200, 'body': 'Processed successfully'}