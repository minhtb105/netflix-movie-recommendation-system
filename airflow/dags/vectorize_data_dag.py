from airflow.decorators import dag, task
from datetime import datetime, timedelta 
from airflow.sensors.external_task import ExternalTaskSensor
from pathlib import Path


RAW_DIR = Path("/root/myproject/netflix-movie-recommendation-system/data/raw")
PROJECT_PYTHON_PATH = "/root/myproject/netflix-movie-recommendation-system/.venv/bin/python3.12"

@dag(
    dag_id='vectorize_features',
    description='vectorize trending metadata features',
    start_date=datetime(2025, 7, 25),
    schedule='0 */6 * * *',  # every 6 hours
    catchup=False,
)
def vectorize_trending_metadata():
    # Step 2: Vectorize & write to Parquet
    @task.external_python(task_id="vectorize_movies", 
                        python=PROJECT_PYTHON_PATH,
                        retries=2, retry_delay=timedelta(minutes=30))
    def process_movies():
        def _process():
            from pipelines.movies_pipeline_tmdb import process_movies_pipeline
            import yaml
            params = yaml.safe_load(open("params.yaml"))["process_trending_movies_tmdb"]
            process_movies_pipeline(params)
            
        _process()
    
    @task.external_python(task_id="vectorize_tv", 
                          python=PROJECT_PYTHON_PATH,
                          retries=2, retry_delay=timedelta(minutes=30))
    def process_tv():
        def _process():
            from pipelines.tv_pipeline_tmdb import process_tv_pipeline 
            import yaml
            params = yaml.safe_load(open("params.yaml"))["process_trending_tv_tmdb"]
            process_tv_pipeline(params)

        _process()


    wait_for_fetch = ExternalTaskSensor(
        task_id="wait_for_fetch_extract_features",
        external_dag_id="fetch_extract_features",
        external_task_id=None,
        poke_interval=60,
        timeout=3600,
    )

    movie_task = process_movies()
    tv_task = process_tv()
    wait_for_fetch >> [movie_task, tv_task]

vectorize_trending_metadata = vectorize_trending_metadata()
