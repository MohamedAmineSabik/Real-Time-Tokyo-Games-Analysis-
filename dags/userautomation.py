from datetime import datetime,timedelta
from airflow import DAG
from airflow.operators.empty import EmptyOperator
default_args={
    'owner':'airflow',
    'start_date' : datetime(2023,6,24,00),
    'retries' : 0
}

dag=DAG(dag_id='userautomation',default_args=default_args,schedule='@daily',catchup=False)
start=EmptyOperator(task_id='start',dag=dag)
end=EmptyOperator(task_id='end',dag=dag)

start >> end
