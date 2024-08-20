import requests
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook

with DAG(
    dag_id='DAG_BD_HOOK',
    description='DAG BD HOOK',
    schedule_interval=None,
    start_date=datetime(2024, 1, 1),
    catchup=False,
) as dag:
    def create_table():
        pg_hook = PostgresHook(postgres_conn_id='postgres')
        pg_hook.run('create table if not exists airflow_bd_hook(id int);', autocommit=True)

    def insert_data():
        pg_hook = PostgresHook(postgres_conn_id='postgres')
        pg_hook.run('insert into airflow_bd_hook values(1);', autocommit=True)

    def select_data(**kwargs):
        pg_hook = PostgresHook(postgres_conn_id='postgres')
        records = pg_hook.get_records('select * from airflow_bd_hook;')
        kwargs['ti'].xcom_push(key='query_result', value=records)

    def print_data(ti):
        task_instance = ti.xcom_pull(key='query_result', task_ids='select_data_task')
        print('Dados da tabela:')
        for row in task_instance:
            print(row)

    create_table_task = PythonOperator(
        task_id='create_table_task',
        python_callable=create_table,
    )

    insert_data_task = PythonOperator(
        task_id='insert_data_task',
        python_callable=insert_data,
    )

    select_data_task = PythonOperator(
        task_id='select_data_task',
        python_callable=select_data,
        provide_context=True,
    )

    print_data_task = PythonOperator(
        task_id='print_data_task',
        python_callable=print_data,
        provide_context=True,
    )

create_table_task >> insert_data_task >> select_data_task >> print_data_task
