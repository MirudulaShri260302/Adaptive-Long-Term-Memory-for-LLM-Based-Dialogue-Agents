# Scalable Product Recommendation System using PySpark

**Uttapreksha Patel & Mirudula Shri Muthukumaran — Northeastern University**
**EECE 5698 – Parallel Processing for Data Analytics**

---

## Overview

This project implements a scalable product recommendation system using **PySpark** and **Apache Spark MLlib**. The system applies collaborative filtering via the **Alternating Least Squares (ALS)** algorithm to generate personalized movie recommendations from large-scale user–item interaction data.

Modern platforms like Netflix, Amazon, and Spotify rely on recommendation systems to surface relevant content from massive catalogs. As datasets grow to millions of interactions, distributed machine learning becomes essential. This project explores how Apache Spark's distributed computing framework can efficiently train recommendation models at scale while maintaining strong predictive performance — and evaluates the parallel scalability gains that come with it.

---

## Objectives

- Build a distributed recommendation system using PySpark
- Implement ALS collaborative filtering for large-scale recommendation tasks
- Compare ALS against simple baseline prediction models
- Evaluate recommendation accuracy using standard metrics
- Analyze parallel scalability and runtime performance across cluster configurations

---

## Dataset

This project uses the **[MovieLens 25M](https://grouplens.org/datasets/movielens/)** dataset, a widely used benchmark for recommendation systems research.

| Statistic | Value |
|---|---|
| Total ratings | 25 million |
| Users | 162,000 |
| Movies | 62,000 |

Each record contains:

| Field | Description |
|---|---|
| `userId` | Unique user identifier |
| `movieId` | Unique movie identifier |
| `rating` | Rating provided by the user |
| `timestamp` | Time the rating was recorded |

---

## Methodology

### 1. Data Processing

The dataset is loaded and processed using PySpark DataFrames for distributed data handling across cluster nodes. Steps include data ingestion, cleaning and preprocessing, train–test splitting, and conversion into Spark MLlib-compatible format.

### 2. Baseline Models

Three simple baseline predictors are implemented as reference benchmarks before training the ALS model:

- Global average rating
- User average rating
- Item average rating

### 3. ALS Collaborative Filtering

The primary model is **Alternating Least Squares (ALS)** from Spark MLlib, which performs matrix factorization on the user–item interaction matrix:

```
R ≈ U × Vᵀ
```

where **U** represents latent user factors and **V** represents latent item factors. This enables prediction of unknown ratings and generation of personalized recommendations.

Key hyperparameters:

- **Rank** — latent factor dimension
- **Regularization parameter**
- **Number of iterations**

---

## Experimental Setup

Experiments are executed on the **Northeastern Explorer/Discovery cluster** using distributed PySpark jobs. System performance is analyzed by varying:

- Number of Spark executors
- Number of partitions
- Dataset size
- Caching strategies

---

## Evaluation Metrics

### Recommendation Accuracy

- **RMSE** — measures prediction error between actual and predicted ratings
- **Precision@K** — evaluates the quality of top-N recommendations

### Distributed System Performance

**Speedup:**
```
Speedup = T(1) / T(N)
```

**Parallel Efficiency:**
```
Efficiency = Speedup / N
```

where *N* is the number of distributed executors.

---

## Expected Results

- ALS outperforms all baseline models in RMSE
- High-quality personalized recommendations via collaborative filtering
- Significant reductions in training time with increased parallel resources
- Clear demonstration of distributed ML pipeline scalability

---

## Project Structure

```
Scalable-Product-Recommendation-System-using-PySpark/
│
├── data/
│   └── movielens_dataset/
│
├── src/
│   ├── data_preprocessing.py
│   ├── baseline_models.py
│   ├── als_training.py
│   └── evaluation.py
│
├── experiments/
│   └── scalability_experiments.py
│
├── results/
│   ├── plots/
│   └── performance_metrics/
│
├── README.md
└── project_report.pdf
```

---

## Technology Stack

- **Python**
- **PySpark** / **Apache Spark MLlib**
- **Northeastern Explorer / Discovery Cluster**
- **Pandas**
- **Matplotlib**

---

## Example Output

The system produces:

- Top-N movie recommendations per user
- RMSE accuracy scores
- Precision@K results
- Speedup and parallel efficiency plots
- Training runtime comparisons across cluster configurations

---

## References

- [MovieLens Dataset](https://grouplens.org/datasets/movielens/)
- [Apache Spark MLlib Documentation](https://spark.apache.org/mllib/)
