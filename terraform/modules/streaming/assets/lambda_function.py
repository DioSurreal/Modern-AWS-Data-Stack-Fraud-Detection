import base64
import json
import os
import boto3
from datetime import datetime

s3 = boto3.client('s3')

def lambda_handler(event, context):
    bucket_name = os.environ['S3_BUCKET']
    now = datetime.now()
    
    # สร้าง Partition Path: silver/year=2026/month=04/day=25/hour=14/
    partition_path = now.strftime("bronze/year=%Y/month=%m/day=%d/hour=%H")
    
    for record in event['Records']:
        # 1. แตกข้อมูลจาก Kinesis
        payload = base64.b64decode(record['kinesis']['data']).decode('utf-8')
        data = json.loads(payload)
        
        if not data.get('account_id') or data.get('amount') is None:
            print(f"Skipping record: Missing essential fields in {data}")
            continue # ข้ามไป Record ถัดไปเลย
        
    # 2. Value Validation: ยอดเงินต้องไม่ติดลบ
        if data['amount'] < 0:
            print(f"Skipping record: Invalid amount {data['amount']}")
            continue
        
        # 2. ทำ Data Enrichment (Silver Layer)
        data['risk_fraud'] = True if data.get('amount', 0) > 300000 else False
        data['processed_at'] = now.isoformat()
        
        # 3. บันทึกลง S3 แยกตาม Partition
        file_name = f"{partition_path}/transaction_{record['kinesis']['sequenceNumber']}.json"
        
        s3.put_object(
            Bucket=bucket_name,
            Key=file_name,
            Body=json.dumps(data)
        )
        
    return {'statusCode': 200, 'body': 'Processed successfully'}