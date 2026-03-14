# Roadmap – Second Brain (Finance)

Living, incremental, and pragmatic roadmap.  
Each version must leave the project usable, even if minimal.

---

## Project objective

Build an application to manage shared finances as a couple, allowing users to:

* View individual and shared income and expenses
* Classify transactions by category
* Maintain simple, clear, and private control
* Scale gradually (web → mobile, manual → bulk)

---

## v0.1 – Technical and conceptual base (Technical MVP)

**Objective:** Have the project base ready and technically functional.

**Scope:**

* Project initialized
* Structure defined
* API running
* Base documentation

**Tasks:**

* [x] Initialize Git repository
* [x] Define project structure
* [x] Create .gitignore
* [x] Create main README.md
* [x] Backend running with FastAPI
* [x] /health endpoint
* [x] Initial technical documentation

---

## v0.2 – Data model and domain

**Objective:** Clearly define the business before building any UI.

**Scope:**

* Clear entities
* Defined relationships
* Data still in memory

**Tasks:**

* [x] Define main entities
  * User
  * Account
  * Transaction
  * Category
* [x] Define shared vs individual concepts
* [x] Document business rules
* [x] Create backend models

---

## v0.3 – Minimal functional backend

**Objective:** Be able to register and query transactions via API.

**Scope:**

* Basic CRUD
* Simple persistence (memory / JSON)

**Tasks:**

* [x] Create transaction endpoints
* [x] Create category endpoints
* [x] Balance calculation service
* [x] Controller / service / repository separation

---

## v0.4 – Basic web frontend

**Objective:** Use the system without relying on external tools.

**Scope:**

* Simple UI
* No authentication yet

**Tasks:**

* [x] Expense list page
* [x] Manual input form
* [x] Category filters
* [x] Individual vs shared view

---

## v0.5 – Bulk import

**Objective:** Easily load historical data.

**Scope:**

* CSV / Excel

**Tasks:**

* [x] Define file format
* [x] Import endpoint
* [x] Data validation
* [x] Error feedback

---

## v0.5.1 – PostgreSQL

**Objective:** Replace local memory for PostgreSQL

**Scope:**

* PostgreSQL

**Tasks:**

* [x] Alembic
* [x] Updated backend
* [x] Create default user

---

## v0.6 – Users and privacy

**Objective:** Basic access control.

**Scope:**

* Simple login
* Local sessions

**Tasks:**

* [ ] Basic authentication
* [ ] User-based data association

---

## v1.0 – Scalability

**Objective:** Long-term usable project.

**Scope:**

* Mobile-ready
* Stable backend

**Future ideas:**

* Mobile app
* Cloud deployment
* Automatic backups

---

**Roadmap rule:** do not move to the next version until the current one is stable.
