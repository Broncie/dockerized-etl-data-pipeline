import sys
import os
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.docker.operators.docker import DockerOperator
from docker.types import Mount
from datetime import datetime, timedelta

PROJECT_ROOT = os.environ["PROJECT_ROOT"]

sys.path.append('/opt/airflow/api-request')
from insert_records import main

default_args = {
    'description': 'A DAG to orchestrate earthquake data retrieval and processing from an external API',
    'start_date': datetime(2026, 1, 14),
    'catchup': False,
}

dag = DAG(
    dag_id = "earthquake-api-dbt-orchestrator",
    default_args = default_args,
    schedule = timedelta(minutes=1)
)

with dag:
    task1 = PythonOperator(
        task_id = 'ingest_data_task',
        python_callable = main
    )

    task2 = DockerOperator(
        task_id='transform_data_task',
        image='ghcr.io/dbt-labs/dbt-postgres:1.9.latest',
        command='run',
        working_dir='/usr/app',
        mounts=[
            Mount(source=f"{PROJECT_ROOT}/dbt/my_project", target="/usr/app", type="bind"),
            Mount(source=f"{PROJECT_ROOT}/dbt/profiles.yml", target="/root/.dbt/profiles.yml", type="bind"),
        ],
        network_mode='earthquake-data-project_my-network',
        docker_url='unix://var/run/docker.sock',
        auto_remove='success'
    )

    task1 >> task2