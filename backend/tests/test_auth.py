def test_register_success(client):
    r = client.post("/api/auth/register", json={
        "email": "newuser@test.com",
        "password": "Secure123!",
        "name": "New User",
    })
    assert r.status_code == 200

def test_register_duplicate_email(client):
    payload = {"email": "dup@test.com", "password": "Secure123!", "name": "A"}
    client.post("/api/auth/register", json=payload)
    r = client.post("/api/auth/register", json=payload)
    assert r.status_code == 400

def test_login_success(client):
    client.post("/api/auth/register", json={
        "email": "login@test.com",
        "password": "Secure123!",
        "name": "Login User",
    })
    r = client.post("/api/auth/login", data={
        "username": "login@test.com",
        "password": "Secure123!",
    })
    assert r.status_code == 200

def test_login_wrong_password(client):
    client.post("/api/auth/register", json={
        "email": "wrong@test.com",
        "password": "Correct123!",
        "name": "Wrong",
    })
    r = client.post("/api/auth/login", data={
        "username": "wrong@test.com",
        "password": "WrongPassword",
    })
    assert r.status_code == 401

def test_login_nonexistent_user(client):
    r = client.post("/api/auth/login", data={
        "username": "nobody@test.com",
        "password": "Whatever123!",
    })
    assert r.status_code == 401

def test_protected_route_without_auth(client):
    r = client.get("/api/transactions")
    assert r.status_code in (401, 403)