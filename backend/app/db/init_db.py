from app.db.base import Base
from app.db.session import engine

# Import all the models
from app.models import user, account, account_owner, category, transaction


def init_db():
    Base.metadata.create_all(bind=engine)