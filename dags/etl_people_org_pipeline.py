from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator

from src.extract import extract_records
from src.transform import transform_records
from src.validate import validate_records
from src.load import init_schema, load_records

default_args = {"owner": "hieu", "retries": 1}

with DAG(
    dag_id="etl_people_org_pipeline",
    default_args=default_args,
    start_date=datetime(2025, 1, 1),
    schedule_interval="@daily",
    catchup=False,
    tags=["etl", "knowledge-graph", "postgres"],
) as dag:

    def _extract(ti):
        raw = extract_records()
        ti.xcom_push(key="raw_records", value=raw)

    def _transform(ti):
        raw = ti.xcom_pull(key="raw_records", task_ids="extract")
        transformed = transform_records(raw)
        ti.xcom_push(key="transformed", value=transformed)

    def _validate(ti):
        transformed = ti.xcom_pull(key="transformed", task_ids="transform")
        validate_records(transformed)

    def _init_schema():
        init_schema()

    def _load(ti):
        transformed = ti.xcom_pull(key="transformed", task_ids="transform")
        load_records(transformed)

    extract = PythonOperator(task_id="extract", python_callable=_extract)
    transform = PythonOperator(task_id="transform", python_callable=_transform)
    validate = PythonOperator(task_id="validate", python_callable=_validate)
    schema = PythonOperator(task_id="init_schema", python_callable=_init_schema)
    load = PythonOperator(task_id="load", python_callable=_load)

    extract >> transform >> validate >> schema >> load