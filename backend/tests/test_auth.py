from http.cookies import SimpleCookie

from app.models.user import User, UserStatus


def test_register_success(client):
    # Should create a new pending user
    r = client.post(
        "/api/auth/register",
        json={"email": "newuser@test.com", "password": "Secure123!", "name": "New User"},
    )
    assert r.status_code == 201
    data = r.json()
    assert "user" in data
    assert data["user"]["email"] == "newuser@test.com"


def test_register_duplicate_email(client):
    # Same email twice should fail with 400
    payload = {"email": "dup@test.com", "password": "Secure123!", "name": "A"}
    client.post("/api/auth/register", json=payload)
    r = client.post("/api/auth/register", json=payload)
    assert r.status_code == 400


def test_login_success(client, db):
    # Pending user is created, then manually activated in DB
    client.post(
        "/api/auth/register",
        json={"email": "login@test.com", "password": "Secure123!", "name": "Login User"},
    )
    u = db.query(User).filter(User.email == "login@test.com").first()
    u.status = UserStatus.active
    db.commit()

    r = client.post(
        "/api/auth/login",
        json={"email": "login@test.com", "password": "Secure123!"},
    )
    assert r.status_code == 200
    data = r.json()
    assert "user" in data
    assert data["user"]["email"] == "login@test.com"
    # Auth cookies should be set
    cookies = SimpleCookie()
    cookies.load(r.headers.get("set-cookie", ""))
    assert "access_token" in cookies


def test_login_wrong_password(client, db):
    client.post(
        "/api/auth/register",
        json={"email": "wrong@test.com", "password": "Correct123!", "name": "W"},
    )
    u = db.query(User).filter(User.email == "wrong@test.com").first()
    u.status = UserStatus.active
    db.commit()

    r = client.post(
        "/api/auth/login",
        json={"email": "wrong@test.com", "password": "WrongPassword"},
    )
    assert r.status_code == 401


def test_login_nonexistent_user(client):
    r = client.post(
        "/api/auth/login",
        json={"email": "nobody@test.com", "password": "Whatever123!"},
    )
    assert r.status_code == 401


def test_login_pending_user_blocked(client):
    # Registered user without manual activation should not be able to log in
    client.post(
        "/api/auth/register",
        json={"email": "pending@test.com", "password": "Secure123!", "name": "Pending"},
    )
    r = client.post(
        "/api/auth/login",
        json={"email": "pending@test.com", "password": "Secure123!"},
    )
    assert r.status_code in (401, 403)


def test_protected_route_without_auth(client):
    # Accessing a protected endpoint without cookies should fail
    r = client.get("/api/transactions")
    assert r.status_code in (401, 403)


def test_me_authenticated(auth_client):
    # Authenticated client should see current user info
    r = auth_client.get("/api/auth/me")
    assert r.status_code == 200
    data = r.json()
    assert "user" in data
    assert data["user"]["email"] == "test@test.com"


def test_logout(auth_client):
    # Logout should clear cookies and still return 200
    r = auth_client.post("/api/auth/logout")
    assert r.status_code == 200


def test_refresh_token_success(auth_client):
    # Use cookies from an authenticated client to hit /auth/refresh
    # auth_client already logged in and has refresh_token cookie set
    r = auth_client.post("/api/auth/refresh")
    assert r.status_code == 200
    data = r.json()
    assert data["message"] == "Token refreshed"


def test_refresh_token_missing(client):
    # No refresh_token cookie should return 401
    r = client.post("/api/auth/refresh")
    assert r.status_code == 401


def test_change_password_success(auth_client, db):
    # Change password for logged-in user with correct current password
    payload = {
        "current_password": "Test1234!",
        "new_password": "NewPass1234!",
    }
    r = auth_client.put("/api/auth/password", json=payload)
    assert r.status_code == 200
    assert r.json()["message"] == "Password updated successfully"

    # Login must now work with the new password
    r_login = auth_client.post(
        "/api/auth/login",
        json={"email": "test@test.com", "password": "NewPass1234!"},
    )
    assert r_login.status_code == 200


def test_change_password_wrong_current(auth_client):
    # Wrong current password should fail with 400
    payload = {
        "current_password": "WrongCurrent123!",
        "new_password": "AnotherPass1234!",
    }
    r = auth_client.put("/api/auth/password", json=payload)
    assert r.status_code == 400
    assert r.json()["detail"] == "Current password is incorrect"