FROM python:3.7
RUN pip install wtforms==2.3.3 && \
    pip install dbt-postgres>=3.7 && \
    pip install SQLAlchemy==1.3.23 && \
    pip install faker>=3.6 && \
    pip install numpy>=3.8 && \
    pip install psycopg2>=3.6 && \
    pip install 'apache-airflow[postgres]==1.10.14'
    
RUN mkdir /project
COPY scripts_airflow/ /project/scripts/

RUN chmod +x /project/scripts/init.sh
ENTRYPOINT [ "/project/scripts/init.sh" ]