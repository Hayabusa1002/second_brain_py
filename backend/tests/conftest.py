import os
import uuid

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

os.environ.setdefault("DATABASE_URL", "sqlite:///./test.db")
os.environ.setdefault("SECRET_KEY", "test-secret-key-for-pytest-only")
os.environ.setdefault("APP_BASE_URL", "http://testserver")
os.environ.setdefault("APP_ENV", "development")

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
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)
    try:
        if os.path.exists("test.db"):
            os.remove("test.db")
    except PermissionError:
        pass


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


def _unique_email(prefix: str) -> str:
    return f"{prefix}-{uuid.uuid4().hex[:10]}@test.com"


def _register_and_activate(client, db, email, password, name, role: UserRole):
    r_reg = client.post(
        "/api/auth/register",
        json={
            "email": email,
            "password": password,
            "name": name,
        },
    )
    assert r_reg.status_code == 201, f"Register failed: {r_reg.status_code} {r_reg.text}"

    user = db.query(User).filter(User.email == email).first()
    assert user is not None, "User not created in DB"

    user.status = UserStatus.active
    user.role = role
    db.commit()
    db.refresh(user)

    r_login = client.post(
        "/api/auth/login",
        json={
            "email": email,
            "password": password,
        },
    )
    assert r_login.status_code == 200, f"Login failed: {r_login.status_code} {r_login.text}"

    return client, user


@pytest.fixture()
def auth_client(client, db):
    email = _unique_email("user")
    password = "Test1234!"
    _, _user = _register_and_activate(
        client,
        db,
        email=email,
        password=password,
        name="Test User",
        role=UserRole.owner,
    )
    return client


@pytest.fixture()
def admin_client(client, db):
    email = _unique_email("admin")
    password = "Admin1234!"
    _, _user = _register_and_activate(
        client,
        db,
        email=email,
        password=password,
        name="Admin User",
        role=UserRole.admin,
    )
    return client


@pytest.fixture()
def auth_user(client, db):
    email = _unique_email("auth-user")
    password = "Test1234!"
    _client, user = _register_and_activate(
        client,
        db,
        email=email,
        password=password,
        name="Auth User",
        role=UserRole.owner,
    )
    return {"client": _client, "user": user, "email": email, "password": password}


@pytest.fixture()
def auth_client_with_account(auth_client):
    r_acc = auth_client.post(
        "/api/accounts",
        json={
            "name": f"Account-{uuid.uuid4().hex[:6]}",
            "type": "individual",
        },
    )
    assert r_acc.status_code == 201, f"Create account failed: {r_acc.status_code} {r_acc.json()}"

    r_cat = auth_client.post(
        "/api/categories",
        json={
            "name": f"Salary-{uuid.uuid4().hex[:6]}",
            "type": "income",
        },
    )
    assert r_cat.status_code == 201, f"Create category failed: {r_cat.status_code} {r_cat.json()}"

    return auth_client, r_acc.json()["id"], r_cat.json()["id"]