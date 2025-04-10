import pandas as pd
import json
import logging
from airflow.utils.log.logging_mixin import LoggingMixin

def extract_data():
    df = pd.read_csv(r'/opt/airflow/dags/glassdoor_jobs.csv')
    return df.to_dict(orient='records')

def transform_data(**context):
    ti = context['ti']
    data = ti.xcom_pull(task_ids = 'loading_data')
    df = pd.DataFrame(data)
    
    print(df.isnull().sum())
    df.drop(['Unnamed: 0','Job Description','Competitors'],axis = 'columns',inplace = True)
    salary_start = df['Salary Estimate'].apply(lambda x : x.split('-')[0])
    df['Company Name'] = df['Company Name'].apply(lambda x : x.split('\n')[0]).astype('str')
    salary_end_1 = df['Salary Estimate'].apply(lambda x : x.split('-')[1].replace('$','').replace('K','000'))
    df['salary_end'] = salary_end_1.apply(lambda x: x.split('(')[0])
    df['salary_start'] = salary_start.apply(lambda x : x.replace('$','').replace('K','000'))
    salary_false_index = df[df['salary_start'] == ''].index
    df.drop(salary_false_index,inplace = True)
    df['salary_start'].loc[[48,477]]='150000'
    a = df['salary_start'].str.extract(r':(\d+)').dropna()
    df.loc[a.index, 'salary_start'] = df.loc[a.index, 'salary_start'].apply(lambda x: int(x.split(':')[-1]))
    df['salary_start'] = df['salary_start'].astype('int64')
    df['salary_end'] = df['salary_end'].str.extract(r'(\d+)')
    df['salary_end'] = df['salary_end'].astype('int64')
    df['salary_estimate'] = df['salary_start'] + df['salary_end'] / 2
    df.drop(['Salary Estimate','salary_start','salary_end'],axis='columns',inplace = True)
    
    return df.to_dict(orient='records')


def generate_insights(**context):
    logger = logging.getLogger(__name__)
    ti = context['ti']
    data = ti.xcom_pull(task_ids='transform_data')
    
    if data is None:
        logger.error("No data pulled from transform_data task")
        return {"error": "No data available"}
    
    df = pd.DataFrame(data)
    
    top_salary_estimate = pd.DataFrame(df.groupby('Job Title')['salary_estimate'].mean()).sort_values(
        by='salary_estimate', ascending=False)[:10]
    logger.info("TOP 10 HIGHEST SALARY POSITIONS")
    logger.info(str(top_salary_estimate.to_dict()))
    
    top_rated_job = pd.DataFrame(df.groupby('Job Title')['Rating'].mean()).sort_values(
        by='Rating', ascending=False)[:10]
    logger.info("TOP 10 HIGHEST RATED POSITIONS")
    logger.info(str(top_rated_job.to_dict()))
    
    return {
        "top_salary_jobs": top_salary_estimate.to_dict(),
        "top_rated_jobs": top_rated_job.to_dict()
    }
    
    
def load_data(**context):
    ti = context['ti']
    data = ti.xcom_pull(task_ids = 'transform_data')
    df = pd.DataFrame(data)
    df.to_csv(r'/opt/airflow/dags/cleaned_data.csv')
    return "Loaded Cleaned data!!!"
    