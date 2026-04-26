from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from docker.types import Mount
from datetime import datetime, timedelta
import os

DBT_PATH = os.environ.get('DBT_HOST_PATH', 'C:/Users/User/Desktop/Fraud-Detection-AWS/dbt')

DBT_MOUNTS = [
    Mount(
        source=DBT_PATH,
        target='/usr/app/dbt',
        type='bind'
    ),
    Mount(
        source=f'{DBT_PATH}/profiles.yml',
        target='/root/.dbt/profiles.yml',
        type='bind'
    ),
]
default_args = {
    'owner': 'Suriya',
    'depends_on_past': False,
    'email_on_failure': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}


with DAG(
    dag_id='fraud_detection_full_pipeline',
    default_args=default_args,
    description='Run dbt transformation hourly',
    schedule='@hourly',
    start_date=datetime(2026, 4, 1),
    catchup=False,
    tags=['dbt', 'fraud_detection'],
) as dag:

    dbt_run = DockerOperator(
        task_id='dbt_run',
        image='ghcr.io/dbt-labs/dbt-redshift:1.8.0',
        command='run --project-dir /usr/app/dbt/fraud_detection --profiles-dir /root/.dbt',
        mounts=DBT_MOUNTS,
        docker_url='unix://var/run/docker.sock',
        network_mode='bridge',
        auto_remove='success',
    )

    dbt_test = DockerOperator(
        task_id='dbt_test',
        image='ghcr.io/dbt-labs/dbt-redshift:1.8.0',
        command='test --project-dir /usr/app/dbt/fraud_detection --profiles-dir /root/.dbt',
        mounts=DBT_MOUNTS,
        docker_url='unix://var/run/docker.sock',
        network_mode='bridge',
        auto_remove='success',
    )

    dbt_run >> dbt_test