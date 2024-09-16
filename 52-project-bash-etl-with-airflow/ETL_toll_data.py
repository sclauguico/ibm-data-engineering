# import the libraries

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago
from datetime import datetime, timedelta

#defining DAG arguments

# You can override them on a per-task basis during operator initialization
default_args = {
    'owner': 'Your name',
    'start_date': days_ago(0),
    'email': ['your email'],
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# defining the DAG
dag = DAG(
    'ETL_toll_data',
    default_args=default_args,
    description='Toll DAG',
    schedule_interval=timedelta(days=1),
)

unzip_data = BashOperator(
    task_id='unzip_data'
    bash_command='tar -xzf /home/project/airflow/dags/finalassignment/tolldata.tgz'
    dag=dag
)

VEHICLE_FILE='/home/project/airflow/dags/finalassignment/vehicle-data.csv'
CSV_FILE='/home/project/airflow/dags/finalassignment/csv_data.csv'
extract_data_from_csv = BashOperator(
    task_id='extract_data_from_csv',
    bash_command=f'cut -d"," -f1-4 {VEHICLE_FILE} > {CSV_FILE}',
    dag=dag
)

TOLL_FILE='/home/project/airflow/dags/finalassignment/tollplaza-data.tsv'
TSV_FILE='/home/project/airflow/dags/finalassignment/tsv_data.csv'
extract_data_from_tsv = BashOperator(
    task_id='extract_data_from_tsv',
    bash_command=f'cut -d -f5-7 {TOLL_FILE} > {TSV_FILE}',
    dag=dag
)

PAYMENT_FILE='/home/project/airflow/dags/finalassignment/payment-data.txt'
FIXED_WIDTH_FILE='/home/project/airflow/dags/finalassignment/fixed_width_data.csv'
extract_data_from_fixed_width = BashOperator(
    task_id='extract_data_from_fixed_width',
    bash_command=f'cut -c59-67 {PAYMENT_FILE} | tr " " "," > {FIXED_WIDTH_FILE}',
    dag=dag
)

EXTRACTED_DATA='/home/project/airflow/dags/finalassignment/extracted_data.csv'
condosolidate_data = BashOperator(
    task_id='consolidate_data',
    bash_command=f'paste {CSV_FILE} {TSV_FILE} {FIXED_WIDTH_FILE} > {EXTRACTED_DATA}',
    dag=dag
)

EXTRACTED_DATA='/home/project/airflow/dags/finalassignment/extracted_data.csv'
TRANSFORMED_DATA='/home/project/airflow/dags/finalassignment/staging/transformed_data.csv'
transform_data = BashOperator(
    task_id='transform_data',
    bash_command=f"awk -F',' '{{OFS=\",\"; $2=toupper($2); print}}' {EXTRACTED_DATA} > {TRANSFORMED_DATA}",
    dag=dag
)

unzip_data >> extract_data_from_csv >> extract_data_from_tsv >> extract_data_from_fixed_width >> consolidate_data >> transform_data
