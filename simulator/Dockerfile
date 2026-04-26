FROM python:3.9-slim
WORKDIR /app
RUN pip install boto3
COPY producer.py .
CMD ["python", "producer.py"]