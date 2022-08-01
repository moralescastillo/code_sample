from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

yesterday = datetime.now() - timedelta(days=1)

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': yesterday,
    'retries': 0
  }

dag =   DAG('dag_test_01', 
          default_args=default_args,
          schedule_interval= '0 0 * * *')

t0 = BashOperator(
    task_id='say_hello',
    bash_command='echo "hello world"',
    dag=dag)


t0