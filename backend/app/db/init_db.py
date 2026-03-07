# app/db/init_db.py
from app.db.base import Base
from app.db.session import engine

# Importa todos los modelos aquí
from app.models import user

def init_db():
    Base.metadata.create_all(bind=engine)