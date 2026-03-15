# Project Structure v0.1

> Living document that describes the project structure and the decisions behind it.

---

## General repository structure

```text
second_brain/
│
├─ docs/
│  ├─ roadmap.md
│  ├─ structure.md
│  ├─ decisions.md
│  │
│  ├─ domain/
│  │  ├─ entities.md
│  │  ├─ use_cases.md
│  │  ├─ business_rules.md
│  │  └─ models.md
│  │
│  └─ features/
│     ├─ bulk_import.md
│     ├─ alembic.bash
│     ├─ docker.bash
│     ├─ generate_hash.py
│     └─ secret_key.py
│
├─ backend/
│  ├─ README.md
│  ├─ requirements.txt
│  ├─ alembic.ini
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
│  │  │  ├─ __init__.py
│  │  │  ├─ user.py
│  │  │  ├─ account.py
│  │  │  ├─ category.py
│  │  │  ├─ transaction.py
│  │  │  └─ account_owner.py
│  │  │
│  │  ├─ controllers/
│  │  │  ├─ transaction_controller.py
│  │  │  ├─ category_controller.py
│  │  │  ├─ account_controller.py
│  │  │  └─ auth_controller.py
│  │  │
│  │  ├─ routers/
│  │  │  ├─ transactions.py
│  │  │  ├─ categories.py
│  │  │  ├─ accounts.py
│  │  │  └─ auth.py
│  │  │
│  │  ├─ services/
│  │  │  ├─ transaction_service.py
│  │  │  ├─ balance_service.py
│  │  │  ├─ category_service.py
│  │  │  ├─ account_service.py
│  │  │  ├─ import_service.py
│  │  │  ├─ auth_service.py
│  │  │  └─ user_service.py
│  │  │
│  │  ├─ repositories/
│  │  │  ├─ transaction_repository.py
│  │  │  ├─ category_repository.py
│  │  │  ├─ account_repository.py
│  │  │  └─ user_repository.py
│  │  │
│  │  ├─ schemas/
│  │  │  ├─ transaction.py
│  │  │  ├─ category.py
│  │  │  ├─ account.py
│  │  │  ├─ bulk_import.py
│  │  │  └─ user.py
│  │  │
│  │  └─ templates/
│  │     ├─ base.html
│  │     │
│  │     ├─ auth/
│  │     │  ├─ login.html
│  │     │  └─ register.html
│  │     │
│  │     ├─ transactions/
│  │     │  ├─ show.html
│  │     │  ├─ add.html
│  │     │  └─ import.html
│  │     │
│  │     └─ features/
│  │        └─ navbar.html
│  │
│  └─migrations/
│     ├─ versions/
│     ├─ env.py
│     ├─ README.md
│     └─ script.py.mako
│
├─ frontend/
│  ├─ README.md
│  └─ web/
│     ├─ css/
│     │
│     └─ js/
│        ├─ api/
│        │  ├─ transactions.js
│        │  ├─ categories.js
│        │  ├─ accounts.js
│        │  ├─ imports.js
│        │  ├─ auth.js
│        │  └─ base.js
│        │
│        ├─ auth/
│        │  ├─ guard.js
│        │  ├─ login.js
│        │  └─ register.js
│        │
│        └─ transactions/
│           ├─ show.js
│           ├─ add.js
│           └─ import.js
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

## Expected evolution

- v0.1 → base structure
- v0.2 → data models
- v0.3 → basic authentication
- v0.4 → shared expenses
- v1.0 → bulk import + mobile

---

> This document must be updated whenever the structure changes.
