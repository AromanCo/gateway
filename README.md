# Perfume Shop Backend (Microservices with FastAPI)

A scalable microservice-based backend for an online perfume shop using **FastAPI**, **Docker**, **PostgreSQL**, and optional **NATS** for event-based communication.

## 🏗 Project Structure

```
perfume-shop-backend/
├── gateway/              # API Gateway
├── auth_service/         # Auth microservice
├── product_service/      # Product microservice
├── shared/               # Shared code
├── docker-compose.yml    # Compose file to orchestrate services
├── .env                  # Global environment variables
└── README.md             # Project documentation
```

## 📦 Services Overview

### 1. `gateway/`

* Entrypoint for all requests
* Routes requests to internal microservices via HTTP
* Includes Swagger (OpenAPI) documentation

### 2. `auth_service/`

* Handles user registration, login, JWT token issuance
* PostgreSQL + SQLAlchemy + Alembic (optional)

### 3. `product_service/`

* Manages products: create, list, update, delete
* PostgreSQL + SQLAlchemy

### 4. `shared/`

* Common utilities and Pydantic schemas (e.g., JWT helper, validation models)

---

## 🚀 Getting Started

### ✅ Prerequisites

* Docker + Docker Compose
* Python 3.10+ (optional for local dev/testing)

### 🔧 Commands

#### 1. Build and Run All Services

```bash
docker-compose up --build
```

#### 2. Run a Single Service (e.g., auth\_service)

```bash
cd auth_service
uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
```

#### 3. Rebuild Containers

```bash
docker-compose down
docker-compose up --build
```

---

## 🧪 Testing

You can use [HTTPie](https://httpie.io/) or [Postman](https://www.postman.com/) to test endpoints:

```bash
http POST localhost:8000/auth/register username=alice password=secret
http POST localhost:8000/products name="Rose Perfume" price=50.0
```

> Swagger Docs:

* Gateway: [http://localhost:8000/docs](http://localhost:8000/docs)
* Auth Service (direct): [http://localhost:8001/docs](http://localhost:8001/docs)
* Product Service (direct): [http://localhost:8002/docs](http://localhost:8002/docs)

---

## 📁 Service Links

* [gateway/](./gateway)
* [auth\_service/](./auth_service)
* [product\_service/](./product_service)
* [shared/](./shared)

---

## 📌 Environment Variables

Each service has its own `.env` file. Sample contents:

```ini
# .env for auth_service
DB_URL=postgresql://user:password@auth_db:5432/auth_db
JWT_SECRET=supersecret
```

---

## 📬 Message Queue (Optional)

* **NATS** is included for asynchronous communication.
* You can publish/subscribe using `nats-py`.

---

## 🛠 To Do

*

---

## 📃 License

MIT License
