# first time
docker compose up --build -d

# (If needed) for reset alembic versions and save it in local
docker compose exec app alembic revision --autogenerate -m "initial schema"
docker cp second_brain-app-1:/app/migrations/versions/. ./migrations/versions/

# (If needed) for ghost register
docker compose exec db psql -U postgres -d second_brain -c "DELETE FROM alembic_version;"

# Run Alembic migrations inside docker
docker compose exec app alembic upgrade head

# Init seed
docker compose exec app python -m app.db.seed

# Execute updates
docker compose up