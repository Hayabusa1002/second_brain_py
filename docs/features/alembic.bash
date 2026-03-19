# 1. Install alembic
pip install alembic
pip freeze > requirements.txt

# 2. Initialize (create migrations/ with base files)
alembic init migrations

# 2.1. Versions history
python -m alembic history

# 2.2. Version already applied
python -m alembic stamp 5a2a3c288ae7

# 3. Modify default migrations/env.py with project's context

# 4. Create firt migration (reed models/ and generate the SQL)
alembic revision --autogenerate -m "initial schema"

# 5. Execute the migration to DB
alembic upgrade head