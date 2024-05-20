import logging
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.decorators import task, dag

# Определение DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 5, 19),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(seconds=5),
}

@dag(default_args=default_args, schedule_interval=None, catchup=False)
def update():

    @task.bash
    def delta_update() -> str:
        cmd = 'PATH_TO_SCRIPT'
        
        logging.info(f'Running command: {cmd}')

        return cmd

    delta_update()


update()
