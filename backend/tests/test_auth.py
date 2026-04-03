def test_register_success(client):
    payload = {
        "email": "register-success@test.com",
        "password": "Secret123!",
        "name": "Register Success",
    }
    r = client.post("/api/auth/register", json=payload)
    assert r.status_code == 201
    data = r.json()
    assert "user" in data
    assert data["user"]["email"] == payload["email"]


def test_register_duplicate_email(client):
    payload = {
        "email": "duplicate@test.com",
        "password": "Secret123!",
        "name": "Duplicate User",
    }
    r1 = client.post("/api/auth/register", json=payload)
    assert r1.status_code == 201

    r2 = client.post("/api/auth/register", json=payload)
    assert r2.status_code == 400


def test_login_success(client, db):
    from app.models.user import User, UserStatus, UserRole

    payload = {
        "email": "login-success@test.com",
        "password": "Secret123!",
        "name": "Login Success",
    }
    r_reg = client.post("/api/auth/register", json=payload)
    assert r_reg.status_code == 201

    user = db.query(User).filter(User.email == payload["email"]).first()
    assert user is not None
    user.status = UserStatus.active
    user.role = UserRole.owner
    db.commit()

    r = client.post(
        "/api/auth/login",
        json={"email": payload["email"], "password": payload["password"]},
    )
    assert r.status_code == 200
    data = r.json()
    assert "user" in data
    assert data["user"]["email"] == payload["email"]


def test_login_wrong_password(client, db):
    from app.models.user import User, UserStatus, UserRole

    payload = {
        "email": "wrong-pass@test.com",
        "password": "Secret123!",
        "name": "Wrong Pass",
    }
    r_reg = client.post("/api/auth/register", json=payload)
    assert r_reg.status_code == 201

    user = db.query(User).filter(User.email == payload["email"]).first()
    assert user is not None
    user.status = UserStatus.active
    user.role = UserRole.owner
    db.commit()

    r = client.post(
        "/api/auth/login",
        json={"email": payload["email"], "password": "BadPassword123!"},
    )
    assert r.status_code == 401


def test_login_nonexistent_user(client):
    r = client.post(
        "/api/auth/login",
        json={"email": "missing@test.com", "password": "Secret123!"},
    )
    assert r.status_code == 401


def test_login_pending_user_blocked(client):
    payload = {
        "email": "pending-login@test.com",
        "password": "Secret123!",
        "name": "Pending Login",
    }
    r_reg = client.post("/api/auth/register", json=payload)
    assert r_reg.status_code == 201

    r = client.post(
        "/api/auth/login",
        json={"email": payload["email"], "password": payload["password"]},
    )
    assert r.status_code == 403


def test_protected_route_without_auth(client):
    r = client.get("/api/auth/me")
    assert r.status_code in (401, 403)


def test_me_authenticated(auth_user):
    client = auth_user["client"]

    r = client.get("/api/auth/me")
    assert r.status_code == 200
    data = r.json()
    assert "user" in data
    assert data["user"]["email"] == auth_user["email"]


def test_logout(auth_client):
    r = auth_client.post("/api/auth/logout")
    assert r.status_code == 200
    assert r.json()["message"] == "Logged out"

    r_me = auth_client.get("/api/auth/me")
    assert r_me.status_code in (401, 403)


def test_refresh_token_success(auth_client):
    r = auth_client.post("/api/auth/refresh")
    assert r.status_code == 200
    assert r.json()["message"] == "Token refreshed"


def test_refresh_token_missing(client):
    r = client.post("/api/auth/refresh")
    assert r.status_code == 401


def test_change_password_success(auth_user, db):
    client = auth_user["client"]
    email = auth_user["email"]

    payload = {
        "current_password": "Test1234!",
        "new_password": "NewPass1234!",
    }
    r = client.put("/api/auth/password", json=payload)
    assert r.status_code == 200
    assert r.json()["message"] == "Password updated successfully"

    r_login = client.post(
        "/api/auth/login",
        json={"email": email, "password": "NewPass1234!"},
    )
    assert r_login.status_code == 200


def test_change_password_wrong_current(auth_client):
    payload = {
        "current_password": "WrongCurrent123!",
        "new_password": "NewPass1234!",
    }
    r = auth_client.put("/api/auth/password", json=payload)
    assert r.status_code == 400