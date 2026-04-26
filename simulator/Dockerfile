FROM python:3.9-slim
WORKDIR /app
RUN pip install boto3
COPY producer.py .
# มึงต้องส่ง AWS Credentials เข้าไปตอนรัน
CMD ["python", "producer.py"]