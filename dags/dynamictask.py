from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from airflow.models.variable import Variable
from airflow.operators.empty import EmptyOperator


import requests


# Function to be executed by the PythonOperator
def print_task(task_name):
   print(f"Executing task: {task_name}")




# List of task names
#task_names = ['task_1', 'task_2', 'task_3', 'task_4', 'task_5', 'task_6', 'task_7']
task_names = Variable.get("task_list", deserialize_json=True)
# Define the DAG
dag = DAG(
'dynamic_task_example',
description='A simple dynamic DAG',
schedule=None, # Define the schedule, 'None' for manual trigger
start_date=datetime(2024, 11, 21),
catchup=False,
)


# Create a start task
start_task = EmptyOperator(
task_id='start',
dag=dag,
)


# Dynamically generate tasks based on task_names
for task_name in task_names:
   task = PythonOperator(
   task_id=task_name,
   python_callable=print_task,
   op_args=[task_name],
   dag=dag,
   )
# Set task dependencies: start -> task -> end
start_task >> task


# Create an end task
end_task = EmptyOperator(
task_id='end',
dag=dag,
)


# Set dependencies: task -> end
for task_name in task_names:
   task = dag.get_task(task_name)


task >> end_task

