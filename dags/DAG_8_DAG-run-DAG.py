from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from datetime import datetime

with DAG(dag_id='DAG_8_DAG-run-DAG',
         description='DAG_8_DAG-run-DAG',
         schedule_interval=None,
         start_date=datetime(2024, 6, 3),
         catchup=False,
         ) as dag:

    task1 = BashOperator(task_id='task1', bash_command='sleep 5')
    task2 = TriggerDagRunOperator(task_id='task2', trigger_dag_id='DAG_9_DAG-runned')

    task1 >> task2