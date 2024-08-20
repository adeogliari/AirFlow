from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.operators.email import EmailOperator
from airflow.sensors.filesystem import FileSensor
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.models import Variable
from airflow.utils.task_group import TaskGroup
from datetime import datetime, timedelta
import json

default_args = {
    'depends_on_past': False,
    'email': ['ad.ogliari@hotmail.com'],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(seconds=10)
}

with DAG(
    dag_id='WindTurbine',
    description='Dados da Turbina',
    schedule_interval=None,
    start_date=datetime(2024, 1, 1),
    catchup=False,
    default_args=default_args,
    default_view='graph',
    doc_md='## Dag para registrar dados de turbina eólica'
) as dag:

    file_sensor_task = FileSensor(
        task_id='file_sensor',
        filepath=Variable.get('windTurbine_data_file_path'),
        fs_conn_id='fs_windTurbine_data_conn',
        poke_interval=10,
    )

    def process_file(**kwargs):
        with open(Variable.get('windTurbine_data_file_path'), 'r') as file:
            data = json.load(file)
            kwargs['ti'].xcom_push(key='idtemp', value=data['idtemp'])
            kwargs['ti'].xcom_push(key='powerfactor', value=data['powerfactor'])
            kwargs['ti'].xcom_push(key='hydraulicpressure', value=data['hydraulicpressure'])
            kwargs['ti'].xcom_push(key='temperature', value=data['temperature'])
            kwargs['ti'].xcom_push(key='timestamp', value=data['timestamp'])

    get_data_task = PythonOperator(
        task_id='get_data',
        python_callable=process_file,
    )

    with TaskGroup('group_database') as group_database:

        create_table_task = PostgresOperator(
            task_id='create_table',
            postgres_conn_id='postgres',
            sql='''CREATE TABLE IF NOT EXISTS windTurbine(
            idtemp varchar,
            powerfactor varchar,
            hydraulicpressure varchar,
            temperature varchar,
            timestamp varchar);'''
        )


        insert_data_task = PostgresOperator(
            task_id='insert_data',
            postgres_conn_id='postgres',
            sql='''INSERT INTO windTurbine (idtemp, powerfactor, hydraulicpressure, temperature, timestamp)
            VALUES (
            '{{ ti.xcom_pull(task_ids="get_data", key="idtemp")}}',
            '{{ ti.xcom_pull(task_ids="get_data", key="powerfactor")}}',
            '{{ ti.xcom_pull(task_ids="get_data", key="hydraulicpressure")}}',
            '{{ ti.xcom_pull(task_ids="get_data", key="temperature")}}',
            '{{ ti.xcom_pull(task_ids="get_data", key="timestamp")}}'
            );'''
        )

        create_table_task >> insert_data_task

    with TaskGroup('group_check_temp') as group_check_temp:

        def avalia_temp(**kwargs):
            number = float(kwargs['ti'].xcom_pull(task_ids='get_data', key='temperature'))
            if number >= 24:
                return 'group_check_temp.send_email_alert'
            else:
                return 'group_check_temp.send_email_normal'

        check_temp_branch = BranchPythonOperator(
            task_id='check_temp_branch',
            python_callable=avalia_temp,
        )

        send_email_alert_task = EmailOperator(
            task_id='send_email_alert',
            to='ad.ogliari@hotmail.com',
            subject='Airflow Alert',
            html_content='''<h3>Alerta de Temperatura.</h3><p>DAG: WindTurbine</p>'''
        )

        send_email_normal_task = EmailOperator(
            task_id='send_email_normal',
            to='ad.ogliari@hotmail.com',
            subject='Airflow Advise',
            html_content='''<h3>Temperaturas Normais.</h3><p>DAG: WindTurbine</p>'''
        )

        check_temp_branch >> [send_email_alert_task, send_email_normal_task]

    file_sensor_task >> get_data_task >> [group_database, group_check_temp]