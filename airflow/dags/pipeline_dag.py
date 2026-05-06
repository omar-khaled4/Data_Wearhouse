from airflow import DAG
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import requests
import json

default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

def trigger_nifi_flow():
    """Trigger NiFi ingestion flow via REST API"""
    nifi_url = "http://host.docker.internal:8443/nifi-api/flow/process-groups/{process_group_id}/run-status"
    headers  = {"Content-Type": "application/json"}
    payload  = {"id": "your-process-group-id", "state": "RUNNING"}
    response = requests.put(nifi_url, headers=headers, json=payload, verify=False)
    print(f"NiFi trigger status: {response.status_code}")

def stop_nifi_flow():
    """Stop NiFi ingestion flow after loading is done"""
    nifi_url = "http://host.docker.internal:8443/nifi-api/flow/process-groups/{process_group_id}/run-status"
    headers  = {"Content-Type": "application/json"}
    payload  = {"id": "your-process-group-id", "state": "STOPPED"}
    response = requests.put(nifi_url, headers=headers, json=payload, verify=False)
    print(f"NiFi stop status: {response.status_code}")

with DAG(
    dag_id='data_warehouse_pipeline',
    default_args=default_args,
    description='Full pipeline: NiFi ingestion → dbt transformation',
    schedule_interval='@daily',
    start_date=datetime(2024, 1, 1),
    catchup=False,
) as dag:

    start_ingestion = PythonOperator(
        task_id='trigger_nifi_ingestion',
        python_callable=trigger_nifi_flow,
    )

    stop_ingestion = PythonOperator(
        task_id='stop_nifi_ingestion',
        python_callable=stop_nifi_flow,
    )

    # Pipeline order: start NiFi → stop NiFi (dbt added later)
    start_ingestion >> stop_ingestion