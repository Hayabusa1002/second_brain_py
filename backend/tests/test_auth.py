def test_register_success(client):
    r = client.post("/api/auth/register", json={
        "email": "newuser@test.com", "password": "Secure123!", "name": "New User",
    })
    assert r.status_code == 201


def test_register_duplicate_email(client):
    payload = {"email": "dup@test.com", "password": "Secure123!", "name": "A"}
    client.post("/api/auth/register", json=payload)
    r = client.post("/api/auth/register", json=payload)
    assert r.status_code == 400


def test_login_success(client, db):
    from app.models.user import User, UserStatus
    client.post("/api/auth/register", json={
        "email": "login@test.com", "password": "Secure123!", "name": "Login User",
    })
    u = db.query(User).filter(User.email == "login@test.com").first()
    u.status = UserStatus.active
    db.commit()
    r = client.post("/api/auth/login", json={
        "email": "login@test.com", "password": "Secure123!",
    })
    assert r.status_code == 200
    assert "user" in r.json()


def test_login_wrong_password(client, db):
    from app.models.user import User, UserStatus
    client.post("/api/auth/register", json={
        "email": "wrong@test.com", "password": "Correct123!", "name": "W",
    })
    u = db.query(User).filter(User.email == "wrong@test.com").first()
    u.status = UserStatus.active
    db.commit()
    r = client.post("/api/auth/login", json={
        "email": "wrong@test.com", "password": "WrongPassword",
    })
    assert r.status_code == 401


def test_login_nonexistent_user(client):
    r = client.post("/api/auth/login", json={
        "email": "nobody@test.com", "password": "Whatever123!",
    })
    assert r.status_code == 401


def test_login_pending_user_blocked(client):
    client.post("/api/auth/register", json={
        "email": "pending@test.com", "password": "Secure123!", "name": "Pending",
    })
    r = client.post("/api/auth/login", json={
        "email": "pending@test.com", "password": "Secure123!",
    })
    assert r.status_code in (401, 403)


def test_protected_route_without_auth(client):
    r = client.get("/api/transactions")
    assert r.status_code in (401, 403)


def test_me_authenticated(auth_client):
    r = auth_client.get("/api/auth/me")
    assert r.status_code == 200
    assert "user" in r.json()


def test_logout(auth_client):
    r = auth_client.post("/api/auth/logout")
    assert r.status_code == 200