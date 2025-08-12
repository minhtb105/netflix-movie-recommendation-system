# 🍿 Netflix Movie Recommender System - Microservices Architecture

**A production-ready microservices-based movie recommendation platform** combining modern ML infrastructure with scalable distributed services.

## 🎯 Key Technologies
* **Machine Learning**: Collaborative filtering (LightFM/ALS), Deep Learning
* **Feature Store**: Feast with Redis online store
* **Data Pipeline**: DVC + Azure Blob Storage, Apache Airflow
* **Experiment Tracking**: MLflow with model registry
* **Streaming**: Kafka + Apache Flink for real-time events
* **Microservices**: FastAPI-based distributed architecture
* **DevOps**: Docker, Kubernetes, CI/CD with GitHub Actions
* **Monitoring**: Evidently for drift detection

---

## 🏗️ Microservices Architecture

```
                    [Load Balancer]
                          |
        ┌─────────────────┼─────────────────┐
        |                 |                 |
   [Web Service]    [Recommend Service] [Feature Store Service]
        |                 |                 |
        └─────────────────┼─────────────────┘
                          |
    ┌─────────────────────┼─────────────────────────┐
    |                     |                         |
[Data Collection]   [Data Processing]        [Train Service]
    |                     |                         |
[Data Ingestion] → [Feature Retrieval] ← [Data Simulation]
    |                     |                         |
    └──── [TMDB Service] ─┴─── [Model Storage] ─────┘
```

## 🔧 Microservices Overview

### Core Services

| Service | Port | Description |
|---------|------|-------------|
| **web_service** | 8000 | Main FastAPI gateway & user interface |
| **recommend_service** | 8001 | Core recommendation engine |
| **feature_store_service** | 8002 | Feast feature serving |
| **data_collection_service** | 8003 | User interaction logging |
| **data_processing_service** | 8004 | ETL and data transformation |
| **train_service** | 8005 | Model training & MLflow integration |
| **feature_retrieval_service** | 8006 | Feature engineering pipeline |
| **data_ingestion_service** | 8007 | External data sources integration |
| **data_simulation_service** | 8008 | RecSim user behavior simulation |
| **tmdb_service** | 8009 | Movie metadata from TMDB API |

---

## 📁 Project Structure

```
netflix-movie-recommendation-system/
├── services/                    # Microservices
│   ├── web_service/            # Main API gateway
│   │   ├── app.py
│   │   ├── templates/
│   │   └── Dockerfile
│   │
│   ├── recommend_service/      # Recommendation engine
│   │   ├── app.py
│   │   ├── models/
│   │   └── Dockerfile
│   │
│   ├── feature_store_service/  # Feast feature serving
│   │   ├── app.py
│   │   ├── feature_store.yaml
│   │   └── Dockerfile
│   │
│   ├── data_collection_service/ # Event logging
│   │   ├── app.py
│   │   ├── kafka_producer.py
│   │   └── Dockerfile
│   │
│   ├── data_processing_service/ # ETL pipeline
│   │   ├── app.py
│   │   ├── processors/
│   │   └── Dockerfile
│   │
│   ├── train_service/          # Model training
│   │   ├── app.py
│   │   ├── trainers/
│   │   └── Dockerfile
│   │
│   ├── feature_retrieval_service/ # Feature engineering
│   │   ├── app.py
│   │   ├── features/
│   │   └── Dockerfile
│   │
│   ├── data_ingestion_service/ # External data sources
│   │   ├── app.py
│   │   ├── ingestors/
│   │   └── Dockerfile
│   │
│   ├── data_simulation_service/ # User simulation
│   │   ├── app.py
│   │   ├── recsim_kafka.py
│   │   └── Dockerfile
│   │
│   └── tmdb_service/           # Movie metadata
│       ├── app.py
│       ├── tmdb_client.py
│       └── Dockerfile
│
├── data/                       # DVC-tracked datasets
│   ├── raw/
│   ├── processed/
│   └── features/
│
├── model/                      # Model artifacts
├── logs/                       # Service logs
├── mlruns/                     # MLflow experiments
├── airflow/                    # Airflow DAGs
├── airflow_env/               # Airflow environment
├── utils/                     # Shared utilities
│
├── docker-compose.yml         # Local development
├── kubernetes/                # K8s deployment manifests
├── .github/workflows/         # CI/CD pipelines
├── dvc.yaml                   # Data pipeline
├── requirements.txt
├── .env.example
└── README.md
```

---

## 🚀 Quick Start

### 1. Prerequisites
```bash
# Required tools
- Docker & Docker Compose
- Python 3.10+
- kubectl (for K8s deployment)
- Azure CLI (for cloud storage)
```

### 2. Environment Setup
```bash
git clone https://github.com/minhtb105/netflix-movie-recommendation-system.git
cd netflix-movie-recommendation-system

# Copy environment variables
cp .env.example .env
# Fill in your credentials (Azure, TMDB API, etc.)

# Install dependencies
pip install -r requirements.txt
```

### 3. Data Pipeline
```bash
# Initialize DVC and pull data
dvc init
dvc pull

# Apply Feast feature store
feast apply
feast materialize-incremental $(date +%F)
```

### 4. Start Services
```bash
# Development mode - all services
docker-compose up -d

# Or start individual services
docker-compose up web_service recommend_service feature_store_service
```

### 5. Access Services
- **Main Application**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **MLflow UI**: http://localhost:5000
- **Airflow UI**: http://localhost:8080

---

## 🔄 Data Flow

### Training Pipeline
```
Data Ingestion → Data Processing → Feature Engineering → Model Training → Model Registry
```

### Inference Pipeline
```
User Request → Web Service → Feature Store → Recommend Service → Response
```

### Real-time Events
```
User Interaction → Data Collection → Kafka → Flink → Data Lake → Feature Store
```

---

## 🧪 API Examples

### Get Recommendations
```bash
curl -X GET "http://localhost:8000/recommend?user_id=123&num_recommendations=10" \
     -H "Content-Type: application/json"
```

### Log User Interaction
```bash
curl -X POST "http://localhost:8003/log_interaction" \
     -H "Content-Type: application/json" \
     -d '{"user_id": 123, "movie_id": 456, "rating": 4.5, "timestamp": "2025-01-01T10:00:00Z"}'
```

### Trigger Model Training
```bash
curl -X POST "http://localhost:8005/train" \
     -H "Content-Type: application/json" \
     -d '{"experiment_name": "lightfm_v1", "hyperparameters": {"learning_rate": 0.01}}'
```

---

## 📊 Monitoring & Observability

### Model Performance
- **MLflow**: Experiment tracking and model versioning
- **Evidently**: Data and model drift detection
- **Custom Metrics**: Precision@K, Recall@K, NDCG

### System Metrics
- **Service Health**: Health check endpoints on each service
- **Performance**: Response time, throughput monitoring
- **Data Quality**: Feature distribution monitoring

---

## 🚢 Deployment

### Docker Compose (Local)
```bash
docker-compose up -d
```

### Kubernetes (Production)
```bash
kubectl apply -f kubernetes/
helm install netflix-recommender ./helm-chart
```

### Cloud Deployment
- **Azure Container Apps**: Managed container deployment
- **AWS EKS**: Kubernetes on AWS
- **GCP Cloud Run**: Serverless container deployment

---

## 🧪 Testing

### Unit Tests
```bash
pytest tests/unit/
```

### Integration Tests
```bash
pytest tests/integration/
```

### Load Testing
```bash
locust -f tests/load/locustfile.py
```

---

## 🤖 Machine Learning Models

### Collaborative Filtering
- **LightFM**: Hybrid matrix factorization with features
- **ALS**: Alternating Least Squares for implicit feedback

### Deep Learning (Future)
- **Neural Collaborative Filtering**: Deep matrix factorization
- **AutoEncoders**: For dimensionality reduction

### Feature Engineering
- User features: demographics, behavior patterns
- Item features: genre, popularity, content features
- Interaction features: temporal patterns, session data

---

## 📈 Performance Benchmarks

| Metric | Target | Current |
|--------|---------|---------|
| Response Time | < 100ms | 85ms |
| Throughput | > 1000 RPS | 1200 RPS |
| Model Accuracy | NDCG@10 > 0.3 | 0.32 |
| Data Freshness | < 1 hour | 45 min |

---

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open Pull Request

---

## 📄 License

MIT License © 2025 Minh TranBinh

---

## 🔗 Links

- **GitHub**: [github.com/minhtb105/netflix-movie-recommendation-system](https://github.com/minhtb105/netflix-movie-recommendation-system)
- **Documentation**: Detailed docs in `/docs` folder
- **Demo Video**: Coming soon!
