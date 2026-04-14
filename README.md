# FastAPI Mongo Clean Architecture

Production-ready FastAPI starter with MongoDB, pagination, and a clean architecture layout.

## Stack

- FastAPI
- PyMongo async client
- Pydantic v2
- Pytest

## Project structure

```text
app/
  api/                # HTTP layer
  application/        # Use-case orchestration
  core/               # Settings and database bootstrap
  domain/             # Entities and repository contracts
  infrastructure/     # MongoDB implementations
  schemas/            # Request/response models
  shared/             # Shared response utilities
tests/
```

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
uvicorn app.main:app --reload
```

## API

- `GET /health`
- `POST /api/v1/items/`
- `GET /api/v1/items/?page=1&page_size=10`
- `GET /api/v1/items/{item_id}`
- `PUT /api/v1/items/{item_id}`
- `DELETE /api/v1/items/{item_id}`

## Example payload

```json
{
  "name": "Laptop",
  "description": "16GB RAM, 1TB SSD",
  "price": 1499.99,
  "quantity": 7
}
```
# fastapi_project
