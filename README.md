# 🏨 Hotel Booking API

An asynchronous REST API service for hotel search and booking, built with **FastAPI**. 

The project follows clean architecture principles (implementing the Data Access Object pattern), supports **API versioning**, and is designed to handle high loads with comprehensive monitoring.

## 🛠 Tech Stack
* **Language:** Python 3.14
* **Framework:** FastAPI, Pydantic
* **Database:** PostgreSQL, SQLAlchemy (asyncpg), Alembic (migrations)
* **Caching:** Redis, fastapi-cache2
* **Search:** Elasticsearch
* **Background Tasks:** Celery
* **Authentication:** JWT tokens (fastapi-users, bcrypt)
* **Monitoring & Observability:** Prometheus, Grafana
* **Admin Panel:** SQLAdmin
* **Testing:** Pytest, pytest-asyncio, httpx

## 🚀 How to run locally

### 1. Clone and setup environment
Clone the repository and navigate to the project directory:
```bash
git clone <your_github_link>
cd project