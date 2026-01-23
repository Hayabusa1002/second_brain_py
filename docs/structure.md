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
│     └─ business_rules.md
│
├─ backend/
│  ├─ README.md
│  ├─ .venv/
│  ├─ app/
│  │  ├─ __init__.py
│  │  ├─ main.py
│  │  │
│  │  ├─ controllers/
│  │  │  └─ health_controller.py
│  │  │
│  │  ├─ services/
│  │  │  └─ __init__.py
│  │  │
│  │  ├─ models/
│  │  │  └─ __init__.py
│  │  │
│  │  └─ repositories/
│  │     └─ __init__.py
│  │
│  └─ requirements.txt
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