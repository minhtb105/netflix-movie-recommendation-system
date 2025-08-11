# 🍿 Netflix Movie Recommender System

**A production-ready template for a real-time movie recommendation platform** combining

* Collaborative filtering (LightFM/ALS)
* Feature Store (Feast)
* Data versioning (DVC + Azure Blob Storage)
* Experiment tracking (MLflow)
* Inference API (FastAPI)
* Streaming & analytics (Kafka → Flink → Data Lake)
* Auto-retraining & drift detection (Evidently, ZenML/Airflow)
* CI/CD pipeline (GitHub Actions)

---

## 📋 Features

* **User & Item Features**: offline and online feature store using Feast
* **Recommendation Model**: LightFM (hybrid) or ALS (matrix factorization)
* **Experiment Tracking**: MLflow logs hyperparameters, metrics, and model artifacts
* **Data Versioning**: DVC pipelines manage raw and processed data with remote storage on Azure Blob
* **Real-time Events**: Click/view events streamed via Kafka, processed by Flink, stored in Data Lake
* **Inference Service**: FastAPI endpoint serving recommendations using real-time features
* **Drift Detection**: Evidently reports identify feature and concept drift
* **Auto-Retraining**: Scheduled retraining pipelines (ZenML or GitHub Actions cron)
* **CI/CD**: Automated build, test, docker image push, and deploy via GitHub Actions

---

## 🏗️ Architecture Overview

```text
[User] → FastAPI (click logging → Kafka)
              ↓
         Kafka Topic (user_events)
              ↓
        Apache Flink Streaming
              ↓
        Data Lake (Parquet partitions)
              ↓
      DVC & Feast Offline Store
              ↓              ↘
        Training Pipeline → MLflow → Model Registry
              ↓                                   ↘
  Retraining Cron / Trigger                      Inference API → FastAPI → Users
              ↑
      Feast Online Store (Redis)
```

---

## ⚙️ Prerequisites

* **OS**: Linux (tested)
* **Docker**
* **Python 3.10+**
* **Azure CLI** (if using Azure Blob remote)
* **kubectl** & **Helm** (optional, for K8s deploy)
* **Kafka**, **Redis**, **Flink** (locally via Docker)

---

## 🚀 Quickstart

1. **Clone the repository**:

   ```bash
   git clone https://github.com/yourname/netflix-recommender-template.git
   cd netflix-recommender-template
   ```

2. **Install Python dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**:

   * Copy `.env.example` to `.env` and fill in credentials:

     ```bash
     cp .env.example .env
     ```
   * Required vars: `AZURE_ACCOUNT`, `AZURE_KEY`, `REDIS_URL`, `MLFLOW_TRACKING_URI`, etc.

4. **Initialize DVC & pull data**:

   ```bash
   dvc pull
   ```

5. **Apply Feast feature store**:

   ```bash
   feast apply
   feast materialize-incremental $(date +%F)
   ```

6. **Run data pipeline** (
   ingest → preprocess → feature) with DVC:

   ```bash
   dvc repro
   ```

7. **Train the recommendation model**:

   ```bash
   python src/train.py
   ```

8. **Launch MLflow UI**:

   ```bash
   mlflow ui --port 5000
   ```

9. **Start the inference API**:

   ```bash
   uvicorn src.api:app --host 0.0.0.0 --port 8000 --reload
   ```

10. **View documentation & test**:

    * Visit `http://localhost:8000/docs` for Swagger UI
    * Test recommendation endpoint:

      ```bash
      curl 'http://localhost:8000/recommend?user_id=1&movie_id=50'
      ```

---

## 🗃️ Project Structure

```
netflix-recommender-template/
├── data/                    # DVC-tracked raw & processed data
│   ├── raw/
│   └── processed/
│
├── src/                     # Application code
│   ├── ingest.py            # Data ingestion
│   ├── preprocess.py        # Data cleaning
│   ├── features/            # Feast definitions & config
│   │   ├── feature_store.yaml
│   │   └── feature_def.py
│   ├── train.py             # Model training & MLflow
│   ├── evaluate_drift.py    # Drift detection (Evidently)
│   ├── api.py               # FastAPI inference
│   └── simulator/           # RecSim + Kafka producer
│       └── recsim_kafka.py
│
├── model/                   # Local model artifacts or MLflow URIs
├── tests/                   # Unit tests (pytest)
│
├── .github/                 # GitHub Actions workflows
│   └── deploy.yml
│
├── Dockerfile               # Containerize FastAPI + simulator
├── dvc.yaml                 # DVC pipeline config
├── dvc.lock
├── requirements.txt
├── .env.example             # Environment variables template
└── README.md                # This file
```

---

## 🔄 CI/CD Pipeline

* **GitHub Actions** defined in `.github/workflows/deploy.yml`:

  * Lint & test (pytest)
  * Build & push Docker image
  * Trigger deployment hook (e.g. Render/Fly.io/Azure)

---

## ☁️ Deployment Options

* **Docker Compose** (local testing)
* **Render/Fly.io**: automatic Docker deploy
* **Azure App Service**: containerized deployment
* **Kubernetes**: Helm chart for FastAPI, Kafka, Redis, Flink

---

## 🎛️ Real-time Simulation & Streaming

1. **RecSim + Kafka**: `src/simulator/recsim_kafka.py` sends simulated user events
2. **Flink Job**: defined in `infra/flink/job.sql` or PyFlink script
3. **Data Lake**: Parquet files partitioned by event type/day under `/data_lake/`

---

## 🤝 Contributing

1. Fork this repo
2. Create a branch: `feature/your-feature`
3. Commit changes & push
4. Open a Pull Request

---

## 📄 License

MIT License © 2025 Minh TranBinh
