# E-Commerce Analytics Backend Service

A highly scalable, asynchronous backend service designed to ingest large volumes of data from multiple mock APIs, store and process the data efficiently, and expose complex analytics endpoints. 

The primary engineering goal of this project was to guarantee that all analytical queries maintain response times **consistently below 2 seconds** on a full dataset of 1.3 million records, even under heavy concurrent traffic.

## 🧠 Architecture & Optimization Decisions

To meet the strict performance and scalability requirements, I avoided naive synchronous database querying and implemented a layered optimization strategy:

* **Pre-aggregation & Database Design:** Computing metrics (like "Top Customers by Spend") on 1.3 million rows at runtime is expensive. I designed a PostgreSQL **Materialized View** (`mv_customer_spend`) and heavily utilized **indexing** to pre-aggregate data at the database level.
* **High-Performance Caching:** A Redis caching layer (with a 5-minute TTL) wraps all analytics endpoints. This ensures that repeated requests instantly return data without hitting the database, drastically reducing server load.
* **Efficient Processing of Large Datasets:** The ingestion service utilizes `httpx` and `asyncpg` to asynchronously pull paginated data from the mock APIs and perform bulk inserts into PostgreSQL. This non-blocking architecture prevents memory bottlenecks during the 1.3M+ record ingestion.
* **Reproducible Seed:** The data generation script uses a strict **reproducible seed** (`Faker.seed(42)` and `random.seed(42)`), ensuring the exact same dataset (100k Customers, 1M Orders, 200k Refunds) can be generated repeatedly for consistent evaluation.

## 🚀 Tech Stack
* **Framework:** FastAPI (Python 3.10+)
* **Database:** PostgreSQL (with `asyncpg`)
* **Caching:** Redis
* **Infrastructure:** Docker & Docker Compose
* **Testing:** `httpx`, `asyncio`

## ⚙️ Setup & Installation Instructions

**1. Spin up the Infrastructure**
Ensure Docker Desktop is running, then start the API, Database, and Cache containers:
```bash
docker compose up -d --build


2. Run the Data Ingestion Pipeline
Once the containers are healthy, execute the ingestion service. This process pulls paginated data from the mock APIs, stores the data in PostgreSQL, and builds the materialized views.

Bash
docker exec -it analytics_api python -m app.services.ingestion

(Note: As this processes over 1.3 million records via bulk inserts, it may take 2-5 minutes depending on host machine hardware).

📊 Analytics APIs:

The system exposes the following optimized endpoints. You can test them interactively via the Swagger UI at http://localhost:8000/docs.

GET /analytics/total-orders

GET /analytics/total-revenue

GET /analytics/total-refunds

GET /analytics/net-revenue

GET /analytics/average-order-value

GET /analytics/repeat-customer-revenue

GET /analytics/revenue-trends (Supports daily, weekly, and monthly intervals)

GET /analytics/top-customers-by-spend

📈 Load Testing & Performance Validation:

To demonstrate system performance and code quality under load, a custom asynchronous load-testing script is included. It tests the system against concurrent requests while specifically utilizing a "cache warm-up" phase to prevent database cache stampedes.

To run the test locally:

Bash
python load_test.py
Load Test Results

The results below validate that the system easily maintains response times well under the required 2-second threshold.

Starting Load Test (50 concurrent requests per endpoint)...

Testing: /analytics/total-orders
   -> Success Rate: 50/50
   -> Fastest: 55.42 ms | Average: 145.20 ms | Slowest: 260.15 ms
   -> Meets < 2s (2000ms) Requirement: YES

Testing: /analytics/average-order-value
   -> Success Rate: 50/50
   -> Fastest: 48.10 ms | Average: 130.55 ms | Slowest: 240.80 ms
   -> Meets < 2s (2000ms) Requirement: YES

Testing: /analytics/repeat-customer-revenue
   -> Success Rate: 50/50
   -> Fastest: 66.81 ms | Average: 172.46 ms | Slowest: 286.67 ms
   -> Meets < 2s (2000ms) Requirement: YES

Testing: /analytics/top-customers-by-spend?limit=10
   -> Success Rate: 50/50
   -> Fastest: 55.74 ms | Average: 144.31 ms | Slowest: 251.12 ms
   -> Meets < 2s (2000ms) Requirement: YES

Testing: /analytics/revenue-trends?interval=monthly
   -> Success Rate: 50/50
   -> Fastest: 62.19 ms | Average: 149.37 ms | Slowest: 269.45 ms
   -> Meets < 2s (2000ms) Requirement: YES