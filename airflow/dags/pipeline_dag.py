from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    "owner": "govind",
    "start_date": datetime(2025, 1, 1),
}

with DAG(
    dag_id="data_pipeline",
    default_args=default_args,
    schedule="@daily",
    catchup=False,
) as dag:

    run_pipeline = BashOperator(
        task_id="run_main_pipeline",
        bash_command="cd /opt/project && python main.py",
    )

    run_pipeline