from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    'depends_on_past': False,
    'start_date': datetime(2024, 6, 12),
    'email': ['teste@teste.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(seconds=10),
}

dag = DAG(
    dag_id='defaultArgs',
    description="Dag para estudar Default Args",
    default_args=default_args,
    schedule_interval='@hourly',
    start_date=datetime(2024, 6, 12),
    catchup=False,
    default_view='graph',
    tags=['processo', 'tag', 'pipeline']
)

task1 = BashOperator(task_id='task1',
                     bash_command='sleep 5',
                     dag=dag, retries=3)

task2 = BashOperator(task_id='task2',
                     bash_command='sleep 5',
                     dag=dag, retries=3)

task3 = BashOperator(task_id='task3',
                     bash_command='sleep 5',
                     dag=dag, retries=3)

task1 >> task2 >> task3
