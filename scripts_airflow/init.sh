#!/usr/bin/env bash

# Setup DB Connection String
AIRFLOW__CORE__SQL_ALCHEMY_CONN="postgresql+psycopg2://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DB}"
export AIRFLOW__CORE__SQL_ALCHEMY_CONN

AIRFLOW__WEBSERVER__SECRET_KEY="openssl rand -hex 30"
export AIRFLOW__WEBSERVER__SECRET_KEY

DBT_POSTGRESQL_CONN="postgresql+psycopg2://${DESTINATION_POSTGRES_USER}:${DESTINATION_POSTGRES_PASSWORD}@${DESTINATION_POSTGRES_HOST}:${POSTGRES_PORT}/${DESTINATION_POSTGRES_DB}"
export DBT_POSTGRESQL_CONN

SOURCE_POSTGRESQL_CONN="postgresql+psycopg2://${SOURCE_POSTGRES_USER}:${SOURCE_POSTGRES_PASSWORD}@${SOURCE_POSTGRES_HOST}:${POSTGRES_PORT}/${SOURCE_POSTGRES_DB}"
export SOURCE_POSTGRESQL_CONN

# cd /dbt && dbt compile
rm -f /airflow/airflow-webserver.pid

sleep 10
airflow upgradedb
sleep 10
airflow connections --add --conn_id 'dbt_postgres_instance_raw_data' --conn_uri $DBT_POSTGRESQL_CONN
airflow scheduler & airflow webserver