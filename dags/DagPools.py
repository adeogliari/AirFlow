from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta


dag = DAG(
    dag_id='pool_dag',
    description="DAG usando Pool",
    schedule_interval='@hourly',
    start_date=datetime(2024, 6, 12),
    catchup=False,
    default_view='graph'
)

task1 = BashOperator(task_id='tsk1', bash_command='sleep 5', dag=dag, pool='my-pool', priority_weight=20)
task2 = BashOperator(task_id='tsk2', bash_command='sleep 5', dag=dag, pool='my-pool', priority_weight=7)
task3 = BashOperator(task_id='tsk3', bash_command='sleep 5', dag=dag, pool='my-pool', priority_weight=5)
task4 = BashOperator(task_id='tsk4', bash_command='sleep 5', dag=dag, pool='my-pool', priority_weight=10)


