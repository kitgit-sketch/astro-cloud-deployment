from airflow import dag
from airflow.operators.python import PythonOperator
from pendulum import datetime
def print_hello():
    print("this is my new dag")

with DAG(
    dag_id='new_dag',
    start_date=datetime(2025,1,1,UTC)
    schedule=None
    catchup=False
 ) as dag:
  hello_task = PythonOperator(task_id="Print_hello_task",python_callable=print_hello)