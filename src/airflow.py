from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator

# Определение DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 5, 19),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'delta_update_dag',
    default_args=default_args,
    description='DAG для запуска скрипта delta_update',
    schedule_interval=timedelta(days=1),
    catchup=False,
)

# Оператор для запуска скрипта delta_update
run_delta_update = BashOperator(
    task_id='run_delta_update',
    bash_command='bash /delt.sh',
    dag=dag,
)

run_delta_update