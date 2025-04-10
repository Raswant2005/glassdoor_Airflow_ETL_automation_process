from dag_functions import extract_data,transform_data,generate_insights,load_data
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime,timedelta

default_args = {
    'owner' : 'airflow',
    'retries' : 2,
    'depends_on_past' : False
}

dag = DAG(
    dag_id = 'Glassdoor_ETL_Analytics',
    start_date = datetime(2025,4,9),
    default_args = default_args,
    schedule_interval = '@daily',
    catchup = False
)

extracting_data = PythonOperator(
    task_id = 'loading_data',
    python_callable = extract_data,
    dag = dag
)

transforming_data = PythonOperator(
    task_id = 'transform_data',
    python_callable = transform_data,
    provide_context = True,
    dag = dag
)

insights_generate = PythonOperator(
    task_id = 'extraing_insights_from_data',
    python_callable = generate_insights,
    provide_context = True,
    dag = dag
)

loading_data = PythonOperator(
    task_id = 'final_stage',
    python_callable = load_data,
    provide_context = True,
    dag = dag
)
    
extracting_data >> transforming_data >> insights_generate >> loading_data

