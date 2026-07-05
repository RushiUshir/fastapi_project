# FastAPI Mongo Clean Architecture

Production-ready FastAPI starter with MongoDB, pagination, and a clean architecture layout.

## Stack

- FastAPI
- PyMongo async client
- Pydantic v2
- Google Gemini API
- Pytest

## Project structure

```text
app/
  core/               # Settings and database bootstrap
  schemas/            # Request/response models
tests/
```

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Create a `.env` file with:

```env
MONGODB_URI=mongodb://localhost:27017
MONGODB_DATABASE=local
MONGODB_ITEMS_COLLECTION=items
GEMINI_API_KEY=your_api_key_here
GEMINI_MODEL=gemini-2.5-flash
```

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
