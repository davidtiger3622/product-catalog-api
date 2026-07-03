# Product Catalog API

[![CI](https://github.com/davidtiger3622/product-catalog-api/actions/workflows/ci.yml/badge.svg)](https://github.com/davidtiger3622/product-catalog-api/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/)

A production-style REST API for managing a product catalog, built to demonstrate clean backend architecture: proper HTTP semantics, JWT authentication, database migrations, automated testing, and CI/CD.

## Features

- Full CRUD for products and categories
- JWT-based authentication protecting write operations
- PostgreSQL with SQLAlchemy ORM
- Versioned database migrations via Alembic
- Input validation with Pydantic
- Automated test suite (pytest) with an isolated test database
- CI pipeline: lint, test, and Docker build on every push
- Fully containerized with Docker Compose

## Live Demo

The API is deployed and live at: **https://product-catalog-api-ktsu.onrender.com**

Interactive documentation: **https://product-catalog-api-ktsu.onrender.com/docs**

> Note: hosted on Render's free tier, which spins down after periods of inactivity. The first request after idle may take 30–60 seconds to respond while the service wakes up.

## Tech Stack

| Layer | Technology |
|---|---|
| Framework | FastAPI |
| Database | PostgreSQL |
| ORM | SQLAlchemy |
| Migrations | Alembic |
| Validation | Pydantic |
| Auth | JWT (python-jose, passlib/bcrypt) |
| Testing | pytest |
| Linting | ruff |
| CI/CD | GitHub Actions |
| Containerization | Docker, Docker Compose |
| Deployment | Render (API), Neon (production database) |

## Architecture

```
┌─────────────┐
│   Client    │  (Browser, Insomnia, curl, etc.)
└──────┬──────┘
       │ HTTPS
       ▼
┌─────────────────────────────────────┐
│              FastAPI                 │
│  ┌─────────────────────────────┐    │
│  │  Routers (auth/categories/    │    │
│  │  products)                    │    │
│  └──────────────┬────────────────┘    │
│                 │                     │
│  ┌──────────────▼────────────────┐    │
│  │  JWT Auth Middleware           │    │
│  │  (protects write operations)   │    │
│  └──────────────┬────────────────┘    │
│                 │                     │
│  ┌──────────────▼────────────────┐    │
│  │  Pydantic Schemas               │    │
│  │  (request/response validation) │    │
│  └──────────────┬────────────────┘    │
│                 │                     │
│  ┌──────────────▼────────────────┐    │
│  │  CRUD layer                    │    │
│  └──────────────┬────────────────┘    │
└─────────────────┼─────────────────────┘
                   │ SQLAlchemy ORM
                   ▼
         ┌───────────────────┐
         │    PostgreSQL      │
         │  (Neon in prod,    │
         │   Docker locally)  │
         └───────────────────┘
```

**Request flow example — creating a product:**
1. Client sends `POST /products/` with a JWT in the `Authorization` header and a JSON body.
2. FastAPI routes the request to the products router.
3. The JWT is validated via a dependency (`get_current_user`); unauthenticated requests are rejected before reaching business logic.
4. The request body is validated against the `ProductCreate` Pydantic schema.
5. The router checks that the referenced `category_id` exists, then delegates to the CRUD layer.
6. SQLAlchemy issues the `INSERT` against PostgreSQL and returns the created row.
7. The response is serialized through the `ProductOut` schema and returned as JSON.

## Screenshots

### Interactive API Documentation (Swagger UI)
![Swagger UI Overview](docs/screenshots/swagger-overview.png)

### Example Request Schema
![Request Example](docs/screenshots/swagger-request-example.png)

### Authenticated Request in Action
![Successful Request](docs/screenshots/successful-request.png)

### Continuous Integration
![CI Passing](docs/screenshots/ci-passing.png)

### Test Suite
![Tests Passing](docs/screenshots/tests-passing.png)


## Getting Started

### Prerequisites

- Docker and Docker Compose
- Python 3.12+ (only needed if running Alembic commands outside Docker)

### Setup

1. Clone the repository
```bash
git clone https://github.com/davidtiger3622/product-catalog-api.git
cd product-catalog-api
```

2. Create a `.env` file in the project root
```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/product_catalog
SECRET_KEY=your-secret-key-here
```
Generate a secure secret key with:
```bash
openssl rand -hex 32
```

3. Start the application
```bash
docker compose up --build
```

The API will be available at `http://localhost:8000`, with interactive documentation at `http://localhost:8000/docs`.

4. Apply database migrations
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
alembic upgrade head
```

### Running Tests

Tests run against a separate `product_catalog_test` database to avoid touching development data.

```bash
docker exec -it product-catalog-api-db-1 psql -U postgres -c "CREATE DATABASE product_catalog_test;"
pytest tests/ -v
```

### Linting

```bash
ruff check .
```
## API Endpoints

### Auth

| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| POST | `/auth/register` | Register a new user | No |
| POST | `/auth/login` | Log in and receive a JWT access token | No |

### Categories

| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| GET | `/categories/` | List all categories | No |
| GET | `/categories/{id}` | Get a single category | No |
| POST | `/categories/` | Create a category | Yes |
| DELETE | `/categories/{id}` | Delete a category | Yes |

### Products

| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| GET | `/products/` | List products (supports `category_id`, `skip`, `limit` query params) | No |
| GET | `/products/{id}` | Get a single product | No |
| POST | `/products/` | Create a product | Yes |
| PUT | `/products/{id}` | Update a product (partial updates supported) | Yes |
| DELETE | `/products/{id}` | Delete a product | Yes |

Full interactive documentation with request/response schemas is available at `/docs` (Swagger UI) or `/redoc` when the server is running.

## Testing with Insomnia or Postman

An OpenAPI specification is included at [`openapi.json`](./openapi.json). Import it directly:

- **Insomnia:** Application menu → Import/Export → Import Data → From File → select `openapi.json`
- **Postman:** Import → File → select `openapi.json`

This generates a full request collection with all endpoints and schemas pre-configured. Since the tokens are short-lived, log in via `/auth/login` after importing and set the `Authorization` header manually for protected requests.