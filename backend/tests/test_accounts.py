from app.models.user import User, UserStatus, UserRole


def test_create_account_with_valid_data_returns_201(auth_client):
    r = auth_client.post(
        "/api/accounts",
        json={"name": "Nequi", "type": "individual"},
    )
    assert r.status_code == 201
    data = r.json()
    assert data["name"] == "Nequi"
    assert data["type"] == "individual"


def test_list_accounts_returns_list(auth_client):
    auth_client.post(
        "/api/accounts",
        json={"name": "Davivienda", "type": "individual"},
    )
    r = auth_client.get("/api/accounts")
    assert r.status_code == 200
    assert isinstance(r.json(), list)


def test_create_account_with_invalid_type_returns_422(auth_client):
    r = auth_client.post(
        "/api/accounts",
        json={"name": "X", "type": "invalid_type"},
    )
    assert r.status_code == 422


def test_delete_account_returns_204(auth_client):
    r = auth_client.post(
        "/api/accounts",
        json={"name": "ToDelete", "type": "individual"},
    )
    assert r.status_code == 201
    account_id = r.json()["id"]

    r_del = auth_client.delete(f"/api/accounts/{account_id}")
    assert r_del.status_code == 204


def test_get_balance_existing_account_returns_200(auth_client):
    r = auth_client.post(
        "/api/accounts",
        json={"name": "Cuenta", "type": "individual"},
    )
    assert r.status_code == 201
    account_id = r.json()["id"]

    r_bal = auth_client.get(f"/api/accounts/{account_id}/balance")
    assert r_bal.status_code == 200
    assert r_bal.json() is not None


def test_get_balance_nonexistent_account_returns_404(auth_client):
    import uuid

    fake_id = uuid.uuid4()
    r_bal = auth_client.get(f"/api/accounts/{fake_id}/balance")
    assert r_bal.status_code == 404


def test_list_active_users_returns_200(auth_client):
    r = auth_client.get("/api/accounts/users/active")
    assert r.status_code == 200
    data = r.json()
    assert "users" in data
    assert isinstance(data["users"], list)


def test_update_account_with_valid_data_returns_200(auth_client):
    r = auth_client.post(
        "/api/accounts",
        json={"name": "Old", "type": "individual"},
    )
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


def test_update_account_not_found_returns_404(auth_client):
    import uuid

    fake_id = uuid.uuid4()
    r_upd = auth_client.put(
        f"/api/accounts/{fake_id}",
        json={"name": "New", "type": "individual"},
    )
    assert r_upd.status_code == 404


def test_assign_owner_to_individual_account_returns_400_when_adding_second_owner(auth_client, db):
    r = auth_client.post(
        "/api/accounts",
        json={"name": "Cuenta", "type": "individual"},
    )
    assert r.status_code == 201, r.text
    account_id = r.json()["id"]

    new_user = User(
        email="other@test.com",
        name="Other",
        password="x",
        status=UserStatus.active,
        role=UserRole.owner,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    r_assign = auth_client.post(f"/api/accounts/{account_id}/owners/{new_user.id}")
    assert r_assign.status_code == 400, r_assign.text
    assert r_assign.json()["detail"] == "Individual accounts can only have one owner"


def test_assign_owner_account_not_found_returns_404(auth_client, db):
    import uuid

    new_user = User(
        email="other2@test.com",
        name="Other 2",
        password="x",
        status=UserStatus.active,
        role=UserRole.owner,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    fake_account_id = uuid.uuid4()
    r_assign = auth_client.post(
        f"/api/accounts/{fake_account_id}/owners/{new_user.id}"
    )
    assert r_assign.status_code == 404


def test_unassign_only_owner_from_individual_account_returns_400(auth_client):
    r = auth_client.post(
        "/api/accounts",
        json={"name": "Cuenta", "type": "individual"},
    )
    assert r.status_code == 201, r.text
    account_id = r.json()["id"]

    account_data = r.json()
    owner_id = account_data["owners"][0]["id"]

    r_unassign = auth_client.delete(f"/api/accounts/{account_id}/owners/{owner_id}")
    assert r_unassign.status_code == 400, r_unassign.text


def test_unassign_owner_account_not_found_returns_404(auth_client, db):
    import uuid

    new_user = User(
        email="owner_nf@test.com",
        name="Owner NF",
        password="x",
        status=UserStatus.active,
        role=UserRole.owner,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    fake_account_id = uuid.uuid4()
    r_unassign = auth_client.delete(
        f"/api/accounts/{fake_account_id}/owners/{new_user.id}"
    )
    assert r_unassign.status_code == 404