from fastapi import FastAPI, HTTPException
import logging
from pipelines.ingest_pipeline import ingest_ml100k_pipeline
from pathlib import Path
import pandas as pd

app = FastAPI()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/ingest")
def run_ingest():
    """
    Trigger MovieLens 100k data ingestion pipeline.
    """
    try:
        logger.info("Starting ingestion pipeline...")
        ingest_ml100k_pipeline()
        logger.info("Ingestion complete.")

        processed_dir = Path("data/processed")
        files = list(processed_dir.glob("*.csv"))

        if not files:
            raise HTTPException(status_code=500, detail="No processed CSV files found.")

        summary = {}
        for file in files:
            df = pd.read_csv(file)
            summary[file.name] = len(df)

        return {
            "status": "success",
            "processed_files": summary
        }
    except Exception as e:
        logger.error(f"Ingestion failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    