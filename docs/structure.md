# Project Structure v0.1

> Living document that describes the project structure and the decisions behind it.

---

## General repository structure

```
second_brain/
│
├─ docs/
│  ├─ roadmap.md
│  ├─ structure.md
│  ├─ decisions.md
│  └─ domain/
│     ├─ entities.md
│     ├─ use_cases.md
│     ├─ business_rules.md
│     └─ models.md
│
├─ backend/
│  ├─ README.md
│  ├─ requirements.txt
│  ├─ .venv/
│  ├─ .env
│  └─ app/
│     ├─ __init__.py
│     ├─ main.py
│     │
│     ├─ core/
│     │  ├─ __init__.py
│     │  └─ config.py
│     │
│     ├─ db/
│     │  ├─ __init__.py
│     │  ├─ base.py
│     │  ├─ session.py
│     │  └─ init_db.py
│     │
│     ├─ controllers/
│     │  └─ __init__.py
│     │
│     ├─ services/
│     │  └─ __init__.py
│     │
│     ├─ models/
│     │  ├─ __init__.py
│     │  ├─ user.py
│     │  ├─ account.py
│     │  ├─ category.py
│     │  ├─ transaction.py
│     │  └─ account_owner.py
│     │
│     └─ repositories/
│        └─ __init__.py
│
├─ frontend/
│  ├─ README.md
│  └─ web/
│     ├─ index.html
│     ├─ css/
│     └─ js/
│
├─ .gitignore
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
Responsible for:
- Global configuration
- env vars
- settings
- logging

### Controllers
Responsible for:
- Receiving HTTP requests
- Basic input validation
- Orchestrating services
- Returning responses

### Services
- Business logic
- Calculation rules
- Aggregations

### DB
Responsible for:
- SQLAlchemy **infraestructure**

### Models
- Domain entities
- Represent business concepts

### Repositories
- Data access
- Initially: memory / CSV
- Later: database

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