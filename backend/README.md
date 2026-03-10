# Backend

REST API for managing personal and shared finances as a couple.

## Responsibilities

- Authentication
- Users and shared accounts
- Income and expenses
- Categories and budgets

## Stack

- FastAPI
- PostgreSQL
- Docker

## Requirements

- Python 3.10+

## Initial Technical Documentation

### Installation

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

### Run server

```bash
uvicorn app.main:app --reload
```

### Stop server

```bash
Ctrl + C
```

### Health endpoint

```html
http://127.0.0.1:8000/health
```
