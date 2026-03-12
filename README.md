# Second Brain

Application to manage personal and shared finances as a couple.

## Objective

Record and analyze income and expenses:

- personal
- shared

with clear categories, budgets, and reports.

## Planned Stack

- Backend: API REST with FastAPI (Python)
- Frontend: React
- Database: PostgreSQL
- Infrastructure: Docker + Ubuntu

## Documentation

- Roadmap: docs/roadmap.md

## Run the project

```bash
cd backend
.venv\Scripts\activate

python -m venv .venv
pip install -r requirements.txt

uvicorn app.main:app --reload
```
