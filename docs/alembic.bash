# 1. Install alembic
pip install alembic
pip freeze > requirements.txt

# 2. Initialize (create migrations/ with base files)
alembic init migrations

# 3. Modify default migrations/env.py with project's context

# 4. Create firt migration (reed models/ and generate the SQL)
alembic revision --autogenerate -m "initial schema"

# 5. Execute the migration to DB
alembic upgrade head