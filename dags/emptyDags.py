from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.empty import EmptyOperator
from datetime import datetime, timedelta


dag = DAG(
    dag_id='exemplo_dummy',
    description="Exemplo Dummy",
    schedule_interval='@hourly',
    start_date=datetime(2024, 6, 12),
    catchup=False,
    default_view='graph'
)

task1 = BashOperator(task_id='tsk1', bash_command='sleep 1', dag=dag)
task2 = BashOperator(task_id='tsk2', bash_command='sleep 1', dag=dag)
task3 = BashOperator(task_id='tsk3', bash_command='sleep 1', dag=dag)
task4 = BashOperator(task_id='tsk4', bash_command='sleep 1', dag=dag)
task5 = BashOperator(task_id='tsk5', bash_command='sleep 1', dag=dag)
empty = EmptyOperator(task_id='tsk_empty', dag=dag)

[task1, task2, task3] >> empty >> [task4, task5]

