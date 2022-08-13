import datetime
import os
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator
import psycopg2
from py_scripts.sql_queries import dest_logs, dest_logs_init
from py_scripts.log_converter import convert_logs


DAG_ID = "log_to_destination_dag"
BASEDIR = '../staging'

destination_conn_args = dict(
    host=os.environ['DESTINATION_POSTGRES_HOST'],
    user=os.environ['DESTINATION_POSTGRES_USER'],
    password=os.environ['DESTINATION_POSTGRES_PASSWORD'],
    dbname=os.environ['DESTINATION_POSTGRES_DB'],
    port=os.environ['POSTGRES_PORT'])


def postgres_init():
    conn = psycopg2.connect(**destination_conn_args)
    cur = conn.cursor() 
    cur.execute(dest_logs_init)
    conn.commit()
    conn.close()


def postgres_destination_callable(**kwargs):
    # get csvs
    log_list = kwargs['task_instance'].xcom_pull(task_ids='log_collection')
    csvs = [log.replace('.log', '.csv') for log in log_list]
    csvs = [f for f in os.listdir('staging') if f in csvs]
    # send logs to database
    conn = psycopg2.connect(**destination_conn_args)
    cur = conn.cursor()
    for f in csvs:
        cur.execute(dest_logs.format(f))
        conn.commit()
        # remove csv
        os.remove(f"{BASEDIR}/{f}")
    conn.close()


def collect_logs():
    log_list = []
    for file in os.listdir(BASEDIR):
        if file.endswith(".log"):
            log_list.append(file)
    return log_list



def remove_logs(**kwargs):
    log_list = kwargs['task_instance'].xcom_pull(task_ids='log_collection')
    for f in log_list:
        os.remove(f"{BASEDIR}/{f}")


with DAG(
    dag_id=DAG_ID,
    start_date=datetime.datetime(2022, 8, 10),
    schedule_interval="@once",
    dagrun_timeout=datetime.timedelta(minutes=60)
) as dag:
    log_collection = PythonOperator(
        task_id = 'log_collection',
        python_callable=collect_logs
    )

    logs_to_csv = PythonOperator(
        task_id = 'logs_to_csv',
        python_callable=convert_logs,
        provide_context=True
    )

    log_init = PythonOperator(
        task_id = 'log_init',
        python_callable=postgres_init
    )

    load_logs = PythonOperator(
        task_id = 'load_logs',
        python_callable=postgres_destination_callable,
        provide_context=True
    )

    rm_logs = PythonOperator(
        task_id = 'rm_logs',
        python_callable=remove_logs,
        provide_context=True
    )

    dbt_logs = BashOperator(
        task_id='dbt_logs', 
        bash_command='cd /dbt && dbt compile --select tag:access_logs \
             && dbt run --select tag:access_logs')


log_collection >> logs_to_csv >> log_init >> load_logs >> dbt_logs >> rm_logs