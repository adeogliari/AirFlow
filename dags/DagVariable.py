from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.models import Variable
from datetime import datetime, timedelta


dag = DAG(
    dag_id='dag_variable',
    description="DAG com Variável",
    schedule_interval='@hourly',
    start_date=datetime(2024, 6, 12),
    catchup=False,
    default_view='graph'
)


def print_variable(**context):
    minha_var = Variable.get('minha_var')
    print(f'O valor da variável é: {minha_var}')


task1 = PythonOperator(task_id='tsk1', python_callable=print_variable, dag=dag)

task1


