import os
import datetime
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from py_scripts.log_generator import generate_logs



DAG_ID = "create_log_dag"


with DAG(
    dag_id=DAG_ID,
    start_date=datetime.datetime(2022, 8, 10),
    schedule_interval="@once",
    dagrun_timeout=datetime.timedelta(minutes=60)
) as dag:
    generate_log1 = PythonOperator(
        task_id = 'generate_log1',
        python_callable=generate_logs
    )

    generate_log2 = PythonOperator(
        task_id = 'generate_log2',
        python_callable=generate_logs
    )

    generate_log3 = PythonOperator(
        task_id = 'generate_log3',
        python_callable=generate_logs
    )


generate_log1 >> generate_log2 >> generate_log3
