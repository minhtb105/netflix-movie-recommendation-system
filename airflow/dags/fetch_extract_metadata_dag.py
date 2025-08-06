import asyncio
from airflow.decorators import dag, task
from datetime import datetime, timedelta 
from pathlib import Path


RAW_DIR = Path("/root/myproject/netflix-movie-recommendation-system/data/raw")
PROJECT_PYTHON_PATH = "/root/myproject/netflix-movie-recommendation-system/.venv/bin/python3.10"

@dag(
    dag_id='fetch_extract_features',
    description='Crawl TMDB trending and extract metadata feature',
    start_date=datetime(2025, 8, 6),
    schedule='0 */6 * * *',  # every 6 hours
    catchup=False,
)
def fetch_extract_trending_metadata_dag():
    @task.external_python(task_id="fetch_extract_trending_metadata", 
                        python=PROJECT_PYTHON_PATH,
                        retries=2, retry_delay=timedelta(minutes=30))
    def _run():
        from steps.fetch_trending import fetch_trending_movie_ids, fetch_trending_tv_ids
        from steps.extract_tmdb_features import extract_features
        from pipelines.tmdb_metadata_pipeline import fetch_tv_metadata, fetch_movie_metadata 
            
        movie_ids = fetch_trending_movie_ids()
        movie_metadata = asyncio.run(fetch_movie_metadata(movie_ids=movie_ids, out_path=f"{RAW_DIR}/trending_movie_metadata.json"))
        tv_ids = fetch_trending_tv_ids()
        tv_metadata = asyncio.run(fetch_tv_metadata(tv_ids=tv_ids, out_path=f"{RAW_DIR}/trending_tv_metadata.json"))
            
        extract_features(movie_metadata, 
                        out_path=f"{RAW_DIR}/trending_movie_features.json",
                        review_out_path=f"{RAW_DIR}/trending_movie_reviews.json",
                        is_tv=False,
                        cast_out_path=f"{RAW_DIR}/trending_movie_cast_metadata.json")
        extract_features(tv_metadata, 
                        out_path=f"{RAW_DIR}/trending_tv_features.json", 
                        is_tv=True,
                        cast_out_path=f"{RAW_DIR}/trending_tv_cast_metadata.json")
    
    _run()

fetch_extract_trending_metadata_dag = fetch_extract_trending_metadata_dag()
