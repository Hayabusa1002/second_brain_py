import pytest
import os
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

os.environ.setdefault("DATABASE_URL", "sqlite:///./test.db")
os.environ.setdefault("SECRET_KEY",   "test-secret-key-for-pytest-only")
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


def _register_and_activate(client, db, email, password, name, role=UserRole.owner):
    """Registra un usuario, lo activa y le asigna el rol indicado directamente en DB."""
    client.post("/api/auth/register", json={
        "email": email, "password": password, "name": name,
    })
    user = db.query(User).filter(User.email == email).first()
    if user:
        user.status = UserStatus.active
        user.role   = role
        db.commit()
        db.refresh(user)
    client.post("/api/auth/login", json={
        "email": email, "password": password,
    })
    return client


@pytest.fixture()
def auth_client(client, db):
    """Cliente con usuario activo, rol owner y sesión iniciada."""
    return _register_and_activate(
        client, db,
        email="test@test.com",
        password="Test1234!",
        name="Test User",
    )


@pytest.fixture()
def auth_client_with_account(auth_client, db):
    """Cliente autenticado con una cuenta y categoría creadas."""
    r_acc = auth_client.post("/api/accounts", json={
        "name": "Bancolombia",
        "type": "individual",
    })
    assert r_acc.status_code == 201, f"Create account failed: {r_acc.status_code} {r_acc.json()}"

    r_cat = auth_client.post("/api/categories", json={
        "name": "Salario",
        "type": "income",
    })
    assert r_cat.status_code == 201, f"Create category failed: {r_cat.status_code} {r_cat.json()}"

    return auth_client, r_acc.json()["id"], r_cat.json()["id"]