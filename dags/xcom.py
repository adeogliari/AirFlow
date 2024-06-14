from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta


dag = DAG(
    dag_id='exemplo_excom',
    description="Exemplo Xcom",
    schedule_interval='@hourly',
    start_date=datetime(2024, 6, 12),
    catchup=False,
    default_view='graph'
)


def task_write(**kwarg):
    kwarg['ti'].xcom_push(key='valorxcom1', value=10200)


def task_read(**kwarg):
    valor = kwarg['ti'].xcom_pull(key='valorxcom1')
    print(f'Valor recuperado: {valor}')


task1 = PythonOperator(task_id='task1',
                       python_callable=task_write,
                       dag=dag)

task2 = PythonOperator(task_id='task2',
                       python_callable=task_read,
                       dag=dag)

task1 >> task2
