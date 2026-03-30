# Project Structure v0.1

> Living document that describes the project structure and the decisions behind it.

---

## General repository structure

```text
second_brain/
│
├─ docs/
│  ├─ structure.md
│  ├─ decisions.md
│  │
│  ├─ roadmap/
│  │  ├─ roadmap.md
│  │  └─ vx.x.x.md
│  │
│  ├─ domain/
│  │  ├─ entities.md
│  │  ├─ use_cases.md
│  │  ├─ business_rules.md
│  │  └─ models.md
│  │
│  └─ features/
│
├─ backend/
│  ├─ README.md
│  ├─ requirements.txt
│  ├─ alembic.ini
│  ├─ pytest.ini
│  ├─ .venv/
│  ├─ .env
│  │
│  ├─ app/
│  │  ├─ main.py
│  │  │
│  │  ├─ core/
│  │  │  ├─ config.py
│  │  │  ├─ security.py
│  │  │  └─ exceptions.py
│  │  │
│  │  ├─ db/
│  │  │  ├─ base.py
│  │  │  ├─ session.py
│  │  │  ├─ init_db.py
│  │  │  ├─ deps.py
│  │  │  └─ seed.py
│  │  │
│  │  ├─ models/
│  │  │
│  │  ├─ controllers/
│  │  │
│  │  ├─ routers/
│  │  │
│  │  ├─ services/
│  │  │
│  │  ├─ repositories/
│  │  │
│  │  ├─ schemas/
│  │  │
│  │  └─ templates/
│  │     ├─ base.html
│  │     ├─ auth/
│  │     ├─ transactions/
│  │     └─ features/
│  │
│  ├─ migrations/
│  │  ├─ versions/
│  │  ├─ env.py
│  │  ├─ README.md
│  │  └─ script.py.mako
│  │
│  └─ tests/
│     ├─ conftest.py
│     └─ test_xxx.py
│
├─ frontend/
│  ├─ README.md
│  └─ web/
│     ├─ sw.js
│     │
│     ├─ css/
│     │
│     └─ js/
│        ├─ api/
│        ├─ accounts/
│        ├─ users/
│        ├─ transactions/
│        ├─ auth/
│        └─ features/
│
├─ .gitignore
│
├─ .dockerignore
├─ docker-compose.yml
├─ Dockerfile
│
└─ README.md
```

---

## Design principles

- **Web first**, mobile app later
- **Manual input first**, then bulk CSV/Excel
- **Personal use first**, then scalable
- **Clear frontend / backend separation**
- **Lightweight (pragmatic) MVC**

---

## Backend – Lightweight MVC

### Core

- Global configuration
- env vars
- settings
- logging

### DB

- SQLAlchemy infraestructure

### Models

- Domain entities
- Represent business concepts

### Controllers

- Receiving HTTP requests
- Basic input validation
- Orchestrating services
- Returning responses

### Routers

- Define API routes
- Mapping HTTP methods and paths to controllers
- Grouping endpoints by resource

### Services

- Business logic
- Calculation rules
- Aggregations

### Repositories

- Data access
- Initially: memory / CSV
- Later: database

### Schemas

- Request validation
- Response serialization
- Defining API data contracts

---

## Frontend

### Phase 1

- HTML + JavaScript
- Fetch API
- No framework

### Future phase

- React / Vue
- Reuses backend without changes

---

> This document must be updated whenever the structure changes.
