import os

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Default environment for tests
os.environ.setdefault("DATABASE_URL", "sqlite:///./test.db")
os.environ.setdefault("SECRET_KEY", "test-secret-key-for-pytest-only")
os.environ.setdefault("APP_BASE_URL", "http://testserver")

from app.main import app
from app.db.base import Base
from app.db.deps import get_db
from app.models.user import User, UserRole, UserStatus

SQLALCHEMY_TEST_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_TEST_URL,
    connect_args={"check_same_thread": False},
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="session", autouse=True)
def setup_db():
    """Create all tables once per test session and drop them at the end."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)
    try:
        if os.path.exists("test.db"):
            os.remove("test.db")
    except PermissionError:
        # On Windows the file can be locked; ignore if we cannot delete it
        pass


@pytest.fixture()
def db():
    """Provide a fresh SQLAlchemy session per test."""
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        # Roll back any uncommitted changes and close the session
        session.rollback()
        session.close()


@pytest.fixture()
def client(db):
    """FastAPI TestClient wired to the test database session."""

    def override_get_db():
        try:
            yield db
        finally:
            # The db session is handled by the db fixture
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app, raise_server_exceptions=True) as c:
        yield c
    app.dependency_overrides.clear()


def _register_and_activate(client, db, email, password, name, role=UserRole.owner):
    """Register a user, activate it, set the given role and log in."""
    client.post(
        "/api/auth/register",
        json={
            "email": email,
            "password": password,
            "name": name,
        },
    )
    user = db.query(User).filter(User.email == email).first()
    if user:
        user.status = UserStatus.active
        user.role = role
        db.commit()
        db.refresh(user)
    client.post(
        "/api/auth/login",
        json={
            "email": email,
            "password": password,
        },
    )
    return client


@pytest.fixture()
def auth_client(client, db):
    """Authenticated client with active user and owner role."""
    return _register_and_activate(
        client,
        db,
        email="test@test.com",
        password="Test1234!",
        name="Test User",
        role=UserRole.owner,
    )


@pytest.fixture()
def admin_client(client, db):
    """Authenticated client with active user and admin role."""
    return _register_and_activate(
        client,
        db,
        email="admin@test.com",
        password="Admin1234!",
        name="Admin User",
        role=UserRole.admin,
    )


@pytest.fixture()
def auth_client_with_account(auth_client, db):
    """Authenticated client with one account and one category already created."""
    r_acc = auth_client.post(
        "/api/accounts",
        json={
            "name": "Bancolombia",
            "type": "individual",
        },
    )
    assert (
        r_acc.status_code == 201
    ), f"Create account failed: {r_acc.status_code} {r_acc.json()}"

    r_cat = auth_client.post(
        "/api/categories",
        json={
            "name": "Salary",
            "type": "income",
        },
    )
    assert (
        r_cat.status_code == 201
    ), f"Create category failed: {r_cat.status_code} {r_cat.json()}"

    return auth_client, r_acc.json()["id"], r_cat.json()["id"]