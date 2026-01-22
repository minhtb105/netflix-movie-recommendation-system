# 🍿 Netflix Movie Recommender System – Modular ML System (Microservice-inspired)

**An end-to-end movie recommendation system focused on ML pipelines, MLOps practices, and clean system modularization**, inspired by microservice principles but implemented as a **modular monolith for simplicity and learning purposes**.

This project emphasizes **recommendation algorithms, data pipelines, experiment tracking, and deployment workflows**, rather than operating a full distributed production microservice system.

---

## 🎯 Key Technologies

* **Machine Learning**: Collaborative Filtering (LightFM), Content-based & Hybrid Recommendation
* **Data Versioning**: DVC (local / cloud-backed)
* **Experiment Tracking**: MLflow (experiments & model registry)
* **ML Pipeline**: Offline training → evaluation → model serving
* **Backend API**: FastAPI
* **System Design**: Modular Monolith (microservice-inspired boundaries)
* **DevOps (Foundational)**: Docker, GitHub Actions
* **Monitoring (Offline)**: Ranking metrics (Precision@K, Recall@K, NDCG)

---

## 🏗️ System Design Overview

The system is implemented as a **modular monolith** with clearly separated components, following ideas from microservice architecture such as **separation of concerns, explicit interfaces, and replaceable modules** — without the operational complexity of a true distributed system.

```
Client / UI
    ↓
FastAPI Application
    ↓
┌───────────────────────────────────────┐
│  Recommendation Module                │
│  - Model inference                    │
│  - Ranking logic                      │
├───────────────────────────────────────┤
│  Data & Feature Module                │
│  - Preprocessing                      │
│  - Feature engineering                │
├───────────────────────────────────────┤
│  Training & Evaluation Module         │
│  - Offline training                   │
│  - Metric evaluation                  │
├───────────────────────────────────────┤
│  Infrastructure Module                │
│  - MLflow                             │
│  - DVC                                │
└───────────────────────────────────────┘
```

---

## 🔧 Module Overview

| Module                  | Responsibility                                |
| ----------------------- | --------------------------------------------- |
| **API Layer**           | Exposes recommendation endpoints via FastAPI  |
| **Recommender Core**    | Collaborative & content-based filtering logic |
| **Feature Pipeline**    | Data preprocessing & feature construction     |
| **Training Pipeline**   | Model training, evaluation, and comparison    |
| **Experiment Tracking** | MLflow-based experiment & model tracking      |

---

## 📁 Project Structure

```
netflix-movie-recommendation-system/
├── src/
│   ├── api/                 # FastAPI endpoints
│   ├── recommender/         # Recommendation algorithms
│   ├── features/            # Feature engineering logic
│   ├── training/            # Model training & evaluation
│   ├── data/                # Data loading & preprocessing
│   └── utils/               # Shared utilities
│
├── data/                    # DVC-tracked datasets
│   ├── raw/
│   ├── processed/
│   └── features/
│
├── mlruns/                  # MLflow experiments
├── docker-compose.yml       # Local development setup
├── .github/workflows/       # CI pipelines
├── dvc.yaml                 # Data pipeline definition
├── requirements.txt
└── README.md
```

---

## 🚀 Quick Start

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
```

Run the API:

```bash
uvicorn src.api.app:app --reload
```

---

## 🔄 ML Workflow

### Training

```
Data Ingestion → Feature Engineering → Model Training → Evaluation → MLflow Logging
```

### Inference

```
User Request → FastAPI → Recommender Core → Ranked Movies
```

---

## 🧪 Evaluation

* Offline evaluation using:

  * Precision@K
  * Recall@K
  * NDCG@K
* Compared collaborative, content-based, and hybrid approaches
* Achieved **NDCG@10 ≈ 0.32**, improving ~20% over popularity baseline

---

## 🧠 Recommendation Models

* **Collaborative Filtering**: LightFM
* **Content-based Filtering**: Genre & metadata features
* **Hybrid Recommender**: Weighted combination of multiple signals

---

## 🎯 Design Notes

* System is intentionally kept as a **modular monolith** to reduce unnecessary complexity.
* Architecture allows future refactoring into microservices if scale or team size justifies it.
* Focus is placed on **ML correctness, reproducibility, and maintainability**, rather than distributed operations.

---

## 📌 Purpose

This project was built to demonstrate:

* End-to-end **recommendation system design**
* Practical **ML & MLOps workflows** (DVC, MLflow)
* Thoughtful use of **system architecture trade-offs**

The scope and design intentionally match an **Intern / Junior ML or AI Engineer level**.

---

## 🤝 Contributing

Pull requests and suggestions are welcome. Please keep changes well-tested and documented.
