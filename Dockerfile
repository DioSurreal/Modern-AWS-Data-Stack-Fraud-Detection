FROM apache/airflow:3.2.1

# ลงแค่ตัว adapter กับตัวเชื่อม airflow เท่านั้น
RUN pip install --no-cache-dir \
    dbt-redshift \
    astronomer-cosmos