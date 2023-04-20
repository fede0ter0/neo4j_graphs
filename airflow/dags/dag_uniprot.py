import datetime, pendulum, os
from airflow import DAG
from airflow.operators.python import PythonOperator
from pipelines import proteins

DAG_ID = os.path.basename(__file__).replace('.py', '')

def pipeline_uniprot():
    proteins.run_pipeline()

with DAG(
    dag_id=DAG_ID,
    schedule="0 0 * * *",
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    catchup=False,
    dagrun_timeout=datetime.timedelta(minutes=60)
) as dag:
    uniprot = PythonOperator(
        task_id="uniprot",
        python_callable=pipeline_uniprot
    )

    uniprot