# first time
docker compose up --build

# Run Alembic migrations inside docker
docker compose exec app alembic upgrade head

# Init seed
docker compose exec app python -m app.db.seed

# Execute updates
docker compose up