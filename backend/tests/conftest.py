import pytest
import os
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

os.environ.setdefault("DATABASE_URL",   "sqlite:///./test.db")
os.environ.setdefault("SECRET_KEY",     "test-secret-key-for-pytest-only")
os.environ.setdefault("APP_BASE_URL",   "http://testserver")

from app.main import app
from app.db.base import Base
from app.db.deps import get_db

SQLALCHEMY_TEST_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_TEST_URL,
    connect_args={"check_same_thread": False},
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="session", autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)
    if os.path.exists("test.db"):
        os.remove("test.db")


@pytest.fixture()
def db():
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.rollback()
        session.close()


@pytest.fixture()
def client(db):
    def override_get_db():
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app, raise_server_exceptions=True) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture()
def auth_client(client):
    """Client with registered user and session cookie active."""
    client.post("/api/auth/register", json={
        "email":    "test@test.com",
        "password": "Test1234!",
        "name":     "Test User",
    })
    # Login usa JSON, no form data
    client.post("/api/auth/login", json={
        "email":    "test@test.com",
        "password": "Test1234!",
    })
    return client


@pytest.fixture()
def auth_client_with_account(auth_client):
    """Cliente authenticated with created account y categories."""
    r_acc = auth_client.post("/api/accounts", json={
        "name": "Bancolombia",
        "type": "individual",
    })
    r_cat = auth_client.post("/api/categories", json={
        "name": "Salario",
        "type": "income",
    })
    return auth_client, r_acc.json()["id"], r_cat.json()["id"]