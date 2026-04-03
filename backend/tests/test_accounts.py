from app.models.user import User, UserStatus, UserRole


def test_create_account(auth_client):
    r = auth_client.post("/api/accounts", json={"name": "Nequi", "type": "individual"})
    assert r.status_code == 201
    data = r.json()
    assert data["name"] == "Nequi"
    assert data["type"] == "individual"


def test_list_accounts(auth_client):
    auth_client.post("/api/accounts", json={"name": "Davivienda", "type": "individual"})
    r = auth_client.get("/api/accounts")
    assert r.status_code == 200
    assert isinstance(r.json(), list)


def test_create_account_invalid_type(auth_client):
    r = auth_client.post("/api/accounts", json={"name": "X", "type": "invalid_type"})
    assert r.status_code == 422


def test_delete_account(auth_client):
    r = auth_client.post("/api/accounts", json={"name": "ToDelete", "type": "individual"})
    assert r.status_code == 201
    account_id = r.json()["id"]

    r_del = auth_client.delete(f"/api/accounts/{account_id}")
    assert r_del.status_code == 204


def test_get_balance_existing_account(auth_client):
    r = auth_client.post("/api/accounts", json={"name": "Cuenta", "type": "individual"})
    assert r.status_code == 201
    account_id = r.json()["id"]

    r_bal = auth_client.get(f"/api/accounts/{account_id}/balance")
    assert r_bal.status_code == 200
    assert r_bal.json() is not None


def test_get_balance_nonexistent_account(auth_client):
    import uuid

    fake_id = uuid.uuid4()
    r_bal = auth_client.get(f"/api/accounts/{fake_id}/balance")
    assert r_bal.status_code == 404


def test_list_active_users(auth_client):
    r = auth_client.get("/api/accounts/users/active")
    assert r.status_code == 200
    data = r.json()
    assert "users" in data
    assert isinstance(data["users"], list)


def test_update_account(auth_client):
    r = auth_client.post("/api/accounts", json={"name": "Old", "type": "individual"})
    assert r.status_code == 201
    account_id = r.json()["id"]

    r_upd = auth_client.put(
        f"/api/accounts/{account_id}",
        json={"name": "New", "type": "individual"},
    )
    assert r_upd.status_code == 200
    data = r_upd.json()
    assert data["id"] == account_id
    assert data["name"] == "New"


def test_update_account_not_found(auth_client):
    import uuid

    fake_id = uuid.uuid4()
    r_upd = auth_client.put(
        f"/api/accounts/{fake_id}",
        json={"name": "New", "type": "individual"},
    )
    assert r_upd.status_code == 404


def test_assign_owner_to_existing_account(auth_client, db):
    r = auth_client.post("/api/accounts", json={"name": "Cuenta", "type": "individual"})
    assert r.status_code == 201
    account_id = r.json()["id"]

    new_user = User(
        email="other@test.com",
        name="Other",
        hashed_password="x",
        status=UserStatus.active,
        role=UserRole.owner,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    r_assign = auth_client.post(f"/api/accounts/{account_id}/owners/{new_user.id}")
    assert r_assign.status_code == 200
    assert r_assign.json()["detail"] == "Owner assigned"


def test_assign_owner_account_not_found(auth_client, db):
    import uuid

    new_user = User(
        email="other2@test.com",
        name="Other 2",
        hashed_password="x",
        status=UserStatus.active,
        role=UserRole.owner,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    fake_account_id = uuid.uuid4()
    r_assign = auth_client.post(f"/api/accounts/{fake_account_id}/owners/{new_user.id}")
    assert r_assign.status_code == 404


def test_unassign_owner_existing_account(auth_client, db):
    # Crear cuenta
    r = auth_client.post("/api/accounts", json={"name": "Cuenta", "type": "individual"})
    assert r.status_code == 201
    account_id = r.json()["id"]

    new_user = User(
        email="owner_to_remove@test.com",
        name="Owner To Remove",
        hashed_password="x",
        status=UserStatus.active,
        role=UserRole.owner,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    r_assign = auth_client.post(f"/api/accounts/{account_id}/owners/{new_user.id}")
    assert r_assign.status_code == 200

    r_unassign = auth_client.delete(f"/api/accounts/{account_id}/owners/{new_user.id}")
    assert r_unassign.status_code == 200
    assert r_unassign.json()["detail"] == "Owner removed"


def test_unassign_owner_account_not_found(auth_client, db):
    import uuid

    new_user = User(
        email="owner_nf@test.com",
        name="Owner NF",
        hashed_password="x",
        status=UserStatus.active,
        role=UserRole.owner,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    fake_account_id = uuid.uuid4()
    r_unassign = auth_client.delete(f"/api/accounts/{fake_account_id}/owners/{new_user.id}")
    assert r_unassign.status_code == 404