# Railway deploy

## Goal

Deploy a full‑stack app on Railway with **three separate services**:

- FastAPI backend (API)
- React frontend (UI)
- PostgreSQL database

## 1. Git release

From your bugfix branch:

```bash
git checkout main
git pull origin main
git merge xxx
git push origin main

git tag -a vx.x.x -m "Release vx.x.x"
git push origin vx.x.x
```

## 2. Repo structure (monorepo)

```txt
project-root/
├── backend/
│   ├── app/
│   ├── requirements.txt
│   └── ...
├── frontend/
│   ├── app/
│   │   └── src/
│   ├── package.json
│   └── ...
└── README.md
```

On Railway you’ll have **one project** with **three services**:

- service: `backend` → `Root Directory = backend/`
- service: `frontend` → `Root Directory = frontend/`
- service: `postgres` → managed DB

## 3. Database service

In Railway:

1. Add a **PostgreSQL** service.
2. Copy the connection string and map it to `DATABASE_URL` in the backend service.

Example env in backend service:

```env
DATABASE_URL=postgresql://USER:PASSWORD@HOST:PORT/DBNAME
SECRET_KEY=some-long-random-string
ENV=production
BACKEND_CORS_ORIGINS=https://your-frontend.up.railway.app
```

## 4. Backend (FastAPI) service

Create a new service connected to the same GitHub repo.

Settings:

- **Root Directory**: `backend/`
- **Install Command**: `pip install -r requirements.txt`
- **Start Command**:  
  `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

Make sure FastAPI uses env vars (e.g. `DATABASE_URL`, `SECRET_KEY`) and CORS is configured with the final frontend URL:

```python
from fastapi.middleware.cors import CORSMiddleware

origins = ["https://your-frontend.up.railway.app"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

Deploy and verify:

- `/health` or similar works.
- API returns data from the Railway Postgres DB.

## 5. Frontend (React/Vite) service

Create another service pointing to the same repo.

Settings:

- **Root Directory**: `frontend/`
- **Install Command**: `npm install`
- **Build Command**: `npm run build`
- **Start Command**: depends on your setup:
  - If using a static adapter: `npm run preview` *or* use Railway’s static build preset.
  - If you use a custom Node server: whatever start script runs it.

Set env var so React calls the backend in Railway:

```env
VITE_API_URL=https://your-backend.up.railway.app/api
```

In your Axios client:

```js
const client = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
})
```

Deploy and confirm:

- The frontend loads on `https://your-frontend.up.railway.app`.
- Network tab shows API calls going to the backend URL (no localhost).

## 6. Migrations

Run DB migrations against the Railway Postgres database:

```bash
alembic upgrade head
```

Run this either:

- from your local machine using the Railway `DATABASE_URL`, or
- from the backend service (Railway run/one‑off command).

## 7. Final checklist

- `main` merged and pushed.
- Tag `v1.3.0` pushed.
- Railway Postgres service created.
- Backend service:
  - root `backend/`
  - env: `DATABASE_URL`, `SECRET_KEY`, `ENV`, `BACKEND_CORS_ORIGINS`
  - API reachable.
- Frontend service:
  - root `frontend/`
  - env: `VITE_API_URL` points to backend.
  - UI loads and talks to API.
- Core flows in production work:
  - login / auth
  - list accounts
  - create / edit / delete accounts
  - owners management
  - admin‑only routes.
