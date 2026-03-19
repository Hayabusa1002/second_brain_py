# Roadmap – Second Brain (Finance)

Living, incremental, and pragmatic roadmap.  
Each version must leave the project usable, even if minimal.

## Project objective

Build an application to manage shared finances as a couple, allowing users to:

- View individual and shared income and expenses
- Classify transactions by category
- Maintain simple, clear, and private control
- Scale gradually (web → mobile, manual → bulk)

## v0.1 – Technical and conceptual base (Technical MVP)

**Objective:** Have the project base ready and technically functional.

**Scope:**

- Project initialized
- Structure defined
- API running
- Base documentation

**Tasks:**

- [x] Initialize Git repository
- [x] Define project structure
- [x] Create .gitignore
- [x] Create main README.md
- [x] Backend running with FastAPI
- [x] /health endpoint
- [x] Initial technical documentation

## v0.2 – Data model and domain

**Objective:** Clearly define the business before building any UI.

**Scope:**

- Clear entities
- Defined relationships
- Data still in memory

**Tasks:**

- [x] Define main entities
  - User
  - Account
  - Transaction
  - Category
- [x] Define shared vs individual concepts
- [x] Document business rules
- [x] Create backend models

## v0.3 – Minimal functional backend

**Objective:** Be able to register and query transactions via API.

**Scope:**

- Basic CRUD
- Simple persistence (memory / JSON)

**Tasks:**

- [x] Create transaction endpoints
- [x] Create category endpoints
- [x] Balance calculation service
- [x] Controller / service / repository separation

## v0.4 – Basic web frontend

**Objective:** Use the system without relying on external tools.

**Scope:**

- Simple UI
- No authentication yet

**Tasks:**

- [x] Expense list page
- [x] Manual input form
- [x] Category filters
- [x] Individual vs shared view

## v0.5 – Bulk import

**Objective:** Easily load historical data.

**Scope:**

- CSV / Excel

**Tasks:**

- [x] Define file format
- [x] Import endpoint
- [x] Data validation
- [x] Error feedback

## v0.5.1 – PostgreSQL

**Objective:** Replace local memory for PostgreSQL

**Scope:**

- PostgreSQL

**Tasks:**

- [x] Alembic
- [x] Updated backend
- [x] Create default user

## v0.6 – Users and privacy

**Objective:** Basic access control.

**Scope:**

- Simple login
- Local sessions

**Tasks:**

- [x] Basic authentication
- [x] User-based data association

## v1.0 – Scalability

**Objective:** Mobile-ready + Stable backend.

**Scope:**

- Mobile-ready frontend
- Stable backend
- Infrastructure

**Tasks:**

### Backend Stable

- [x] User roles (`owner` / `partner`)
- [x] Endpoint `GET /accounts` filter by user
- [x] Endpoint `POST /transactions` assign `created_by` from token (not from body)
- [x] Errors management (400, 401, 404, 422 with consistent messages)
- [x] Environment variables `.env` validated (pydantic settings)

### Mobile-ready frontend

- [x] Layout responsive (CSS Grid/Flexbox base)
- [x] Correct viewport in all the templates
- [x] Usable forms in mobile

### Infrastructure

- [x] Functional `docker-compose.yml` (app + PostgreSQL)
- [x] Deploy on cloud server (Railway, Render, or VPS)

---

## v2.0 – User management and account module

**Objective:** Controlled access, admin role, and full account management.

**Scope:**

- Registration with approval flow
- Admin role
- Full accounts CRUD
- Password change

**Tasks:**

### User management

- [x] Registration sets user status to `pending` — no redirect to home
- [x] Post-registration screen: "Your account is pending approval"
- [x] `admin` role as approver of new users
- [ ] Admin view with pending users list (Approve / Reject)
- [ ] Password change (validate current password + new password)
- [ ] Forgot password flow via email

### Accounts module

- [ ] Create, edit, and delete accounts
- [ ] Manage `account_owners` (assign / unassign)
- [ ] Role-based permissions: only admin can create/delete; users see only their own

### Authentication and security

- [ ] Automatic refresh tokens to avoid manual expirations
- [ ] OAuth with Google / GitHub as login option

### User experience

- [ ] Offline mode with Service Workers
- [ ] Global search with filters (type, tag, date)
- [ ] Dark / Light mode

### Core features

- [ ] Markdown or WYSIWYG editor
- [ ] Tags and categories for notes
- [ ] Note linking (backlinks)
- [ ] Export content to PDF / Markdown

### Infrastructure v2.0

- [ ] Automated tests for critical endpoints
- [ ] CI/CD with GitHub Actions
- [ ] Automated release pipeline with `.zip`

---

**Roadmap rule:** do not move to the next version until the current one is stable.
