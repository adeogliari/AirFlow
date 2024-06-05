from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

with DAG(dag_id='DAG_9_DAG-runned',
         description='DAG_9_DAG-runned',
         schedule_interval=None,
         start_date=datetime(2024, 6, 3),
         catchup=False,
         ) as dag:

    task1 = BashOperator(task_id='task1', bash_command='sleep 5')
    task2 = BashOperator(task_id='task2', bash_command='sleep 5')

    task1 >> task2
