import datetime
import os
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.bash_operator import BashOperator
import psycopg2
from py_scripts.sql_queries import company_catalogue_query, \
    supplier_inventory_query, company_order_query, customer_order_query, \
    company_query, customers_query, products_query, suppliers_query, \
    dest_suppliers, dest_products, dest_customers, dest_company, \
    dest_customer_order, dest_company_order, dest_supplier_inventory, \
    dest_company_catalogue

DAG_ID = "source_to_destination_dag"

source_conn_args = dict(
    host=os.environ['SOURCE_POSTGRES_HOST'],
    user=os.environ['SOURCE_POSTGRES_USER'],
    password=os.environ['SOURCE_POSTGRES_PASSWORD'],
    dbname=os.environ['SOURCE_POSTGRES_DB'],
    port=os.environ['POSTGRES_PORT'])

destination_conn_args = dict(
    host=os.environ['DESTINATION_POSTGRES_HOST'],
    user=os.environ['DESTINATION_POSTGRES_USER'],
    password=os.environ['DESTINATION_POSTGRES_PASSWORD'],
    dbname=os.environ['DESTINATION_POSTGRES_DB'],
    port=os.environ['POSTGRES_PORT'])


#  'split --lines 1 > /staging/customer_order_\$FILE.csv'
def postgres_source_callable(**kwargs):
    conn = psycopg2.connect(**source_conn_args)
    cur = conn.cursor()
    cur.execute(kwargs['query'])
    conn.close()


def postgres_destination_callable(**kwargs):
    conn = psycopg2.connect(**destination_conn_args)
    cur = conn.cursor()
    cur.execute(kwargs['query'])
    conn.commit()
    conn.close()
    os.remove(f"{kwargs['file']}")


with DAG(
    dag_id=DAG_ID,
    start_date=datetime.datetime(2022, 8, 10),
    schedule_interval="@once",
    dagrun_timeout=datetime.timedelta(minutes=60)
) as dag:
    s_supplier = PythonOperator(
        task_id = 'source_supplier_query',
        python_callable=postgres_source_callable,
        op_kwargs={'query':suppliers_query}
    )

    d_supplier = PythonOperator(
        task_id = 'destination_supplier_query',
        python_callable=postgres_destination_callable,
        op_kwargs={'query':dest_suppliers, 'file':'/staging/suppliers.csv'}
    )

    s_products = PythonOperator(
        task_id = 'source_products_query',
        python_callable=postgres_source_callable,
        op_kwargs={'query':products_query}
    )

    d_products = PythonOperator(
        task_id = 'destination_products_query',
        python_callable=postgres_destination_callable,
        op_kwargs={'query':dest_products, 'file':'/staging/products.csv'}
    )

    s_customers = PythonOperator(
        task_id = 'source_customers_query',
        python_callable=postgres_source_callable,
        op_kwargs={'query':customers_query}
    )

    d_customers = PythonOperator(
        task_id = 'destination_customers_query',
        python_callable=postgres_destination_callable,
        op_kwargs={'query':dest_customers, 'file':'/staging/customers.csv'}
    )

    s_company = PythonOperator(
        task_id = 'source_company_query',
        python_callable=postgres_source_callable,
        op_kwargs={'query':company_query}
    )

    d_company = PythonOperator(
        task_id = 'destination_company_query',
        python_callable=postgres_destination_callable,
        op_kwargs={'query':dest_company, 'file':'/staging/company.csv'}
    )

    s_customer_order = PythonOperator(
        task_id = 'source_customer_order',
        python_callable=postgres_source_callable,
        op_kwargs={'query':customer_order_query}
    )

    d_customer_order = PythonOperator(
        task_id = 'destination_customer_order_query',
        python_callable=postgres_destination_callable,
        op_kwargs={'query':dest_customer_order, 'file':'/staging/customer_order.csv'}
    )

    s_company_order = PythonOperator(
        task_id = 'source_company_order',
        python_callable=postgres_source_callable,
        op_kwargs={'query':company_order_query}
    )

    d_company_order = PythonOperator(
        task_id = 'destination_company_order_query',
        python_callable=postgres_destination_callable,
        op_kwargs={'query':dest_company_order, 'file':'/staging/company_order.csv'}
    )

    s_supplier_inventory = PythonOperator(
        task_id = 'source_supplier_inventory',
        python_callable=postgres_source_callable,
        op_kwargs={'query':supplier_inventory_query}
    )

    d_supplier_inventory = PythonOperator(
        task_id = 'destination_supplier_inventory_query',
        python_callable=postgres_destination_callable,
        op_kwargs={'query':dest_supplier_inventory, 'file':'/staging/supplier_inventory.csv'}
    )

    s_company_catalogue = PythonOperator(
        task_id = 'source_company_catalogue',
        python_callable=postgres_source_callable,
        op_kwargs={'query':company_catalogue_query}
    )

    d_company_catalogue = PythonOperator(
        task_id = 'destination_company_catalogue_query',
        python_callable=postgres_destination_callable,
        op_kwargs={'query':dest_company_catalogue, 'file':'/staging/company_catalogue.csv'}
    )

    sensors_complete = DummyOperator(task_id='sensor_source_to_destination')

    dbt_source_to_destination = BashOperator(
        task_id='dbt_source_to_destination', 
        bash_command='cd /dbt && dbt compile --select tag:sourcePostgres \
             && dbt run --select tag:sourcePostgres')

[s_supplier >> d_supplier,
s_products >> d_products,
s_customers >> d_customers,
s_company >> d_company,
s_customer_order >> d_customer_order,
s_company_order >> d_company_order,
s_supplier_inventory >> d_supplier_inventory,
s_company_catalogue >> d_company_catalogue] >> sensors_complete >> dbt_source_to_destination