# E-Commerce Analytics Backend Service

## Overview

A high-performance backend analytics platform built with **Python, FastAPI, PostgreSQL, Redis, and Docker**. The system simulates a real-world e-commerce data pipeline by generating large-scale datasets, exposing paginated mock APIs, ingesting millions of records into PostgreSQL, and serving business analytics with sub-2-second response times.

This project was designed to demonstrate backend engineering concepts including data ingestion, API design, database optimization, caching, materialized views, batch processing, and scalable analytics architecture.

### Dataset Scale

* **100,000 Customers**
* **1,000,000 Orders**
* **200,000 Refunds**
* **1.3 Million Total Records**

All datasets are generated using a fixed random seed to ensure reproducibility across environments.

---

## System Architecture

```text
                 ┌────────────────────┐
                 │  Data Generator    │
                 │ (Faker + Seed 42)  │
                 └─────────┬──────────┘
                           │
                           ▼
                 ┌────────────────────┐
                 │     Mock APIs      │
                 │ Customers/Orders   │
                 │     /Refunds       │
                 └─────────┬──────────┘
                           │
                           ▼
                 ┌────────────────────┐
                 │ Ingestion Service  │
                 │ Async Pagination   │
                 │ Batch Processing   │
                 └─────────┬──────────┘
                           │
                           ▼
                 ┌────────────────────┐
                 │    PostgreSQL      │
                 │  Indexed Tables    │
                 └─────────┬──────────┘
                           │
          ┌────────────────┴────────────────┐
          ▼                                 ▼
 ┌───────────────────┐          ┌───────────────────┐
 │ Materialized View │          │   Redis Cache     │
 │ Customer Spend    │          │ Analytics Cache   │
 └─────────┬─────────┘          └─────────┬─────────┘
           │                              │
           └──────────────┬───────────────┘
                          ▼
                ┌────────────────────┐
                │   Analytics API    │
                │  FastAPI Endpoints │
                └────────────────────┘
```

---

## Technology Stack

| Component         | Technology   |
| ----------------- | ------------ |
| Backend Framework | FastAPI      |
| Language          | Python 3.10+ |
| Database          | PostgreSQL   |
| Cache             | Redis        |
| ORM               | SQLAlchemy   |
| Async HTTP Client | HTTPX        |
| Data Generation   | Faker        |
| Containerization  | Docker       |
| Load Testing      | Locust       |

---

## Features

### Data Generation

* Deterministic dataset generation using Faker.
* Fixed seed for reproducibility.
* Generates customers, orders, and refunds at scale.

### Mock APIs

* Paginated endpoints.
* Supports efficient ingestion.
* Simulates external data providers.

### Ingestion Pipeline

* Handles API pagination automatically.
* Async batch processing.
* Efficient bulk insertion into PostgreSQL.

### Analytics APIs

* Total Orders
* Total Revenue
* Total Refunds
* Net Revenue
* Average Order Value (AOV)
* Repeat Customer Revenue
* Revenue Trends
* Top Customers by Spend

### Performance Optimization

* PostgreSQL indexing on critical columns.
* Materialized Views for heavy aggregations.
* Redis caching for frequently accessed metrics.
* Optimized SQL queries and async processing.

---

## API Endpoints

### Mock APIs

```http
GET /mock/customers
GET /mock/orders
GET /mock/refunds
```

### Analytics APIs

```http
GET /analytics/total-orders
GET /analytics/total-revenue
GET /analytics/total-refunds
GET /analytics/net-revenue
GET /analytics/average-order-value
GET /analytics/repeat-customer-revenue
GET /analytics/revenue-trends
GET /analytics/top-customers
```

Interactive API documentation is available at:

```http
http://localhost:8000/docs
```

#Analytics Performance Proof
<img width="1920" height="1200" alt="image" src="https://github.com/user-attachments/assets/3711d29c-276d-4868-8ec8-6c81a8d7cc5e" />

---

## Performance

The system is designed to handle over **1.3 million records** while maintaining analytics response times below **2 seconds** through:

* Database indexing
* Redis caching
* Materialized Views
* Async processing
* Batch ingestion

---

## Running the Project

```bash
docker compose up -d --build
```

Access:

```text
API Docs : http://localhost:8000/docs
PostgreSQL : localhost:5432
Redis : localhost:6379
```
#Architecture Diagram
## System Architecture

```mermaid
flowchart TD

    A[Data Generator<br/>Faker + Seed 42]

    A --> B[Mock API Service]

    B --> B1["/mock/customers"]
    B --> B2["/mock/orders"]
    B --> B3["/mock/refunds"]

    B1 --> C[Ingestion Service]
    B2 --> C
    B3 --> C

    C --> D[Pagination Handler]
    D --> E[Batch Processing]

    E --> F[(PostgreSQL)]

    F --> G[Customers Table]
    F --> H[Orders Table]
    F --> I[Refunds Table]

    H --> J[Indexes]
    I --> J

    F --> K[Materialized Views]
    F --> L[Revenue Aggregations]

    K --> M[Analytics Service]
    L --> M

    N[(Redis Cache)] --> M

    M --> O["/analytics/total-orders"]
    M --> P["/analytics/total-revenue"]
    M --> Q["/analytics/total-refunds"]
    M --> R["/analytics/net-revenue"]
    M --> S["/analytics/average-order-value"]
    M --> T["/analytics/repeat-customer-revenue"]
    M --> U["/analytics/revenue-trends"]
    M --> V["/analytics/top-customers"]

    O --> W[Dashboard / Client]
    P --> W
    Q --> W
    R --> W
    S --> W
    T --> W
    U --> W
    V --> W
```
#Swagger Docs
<img width="1920" height="1200" alt="image" src="https://github.com/user-attachments/assets/c0cf42ec-e5e8-4e6b-8aa2-efabb99e97d8" />

#testing results 

<img width="347" height="499" alt="image" src="https://github.com/user-attachments/assets/2dac5033-33f7-4062-a1d6-55d4535d902d" />

---

## Author

**Vansh Jayswal**

Backend Developer | Python Developer

GitHub: https://github.com/vanshjayswal08-byte

LinkedIn: https://linkedin.com/in/vanshjayswal08
