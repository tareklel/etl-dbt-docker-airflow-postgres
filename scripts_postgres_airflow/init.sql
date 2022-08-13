ALTER ROLE airflowuser SET search_path TO airflow;
CREATE SCHEMA IF NOT EXISTS airflow AUTHORIZATION airflowuser;
SET datestyle = "ISO, DMY";
