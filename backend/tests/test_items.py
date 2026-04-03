import uuid


def test_list_items_by_transaction_returns_200_for_existing_transaction(auth_client_with_account):
    client, account_id, category_id = auth_client_with_account

    r_tx = client.post(
        "/api/transactions",
        json={
            "date": "2026-01-15",
            "amount": 50000,
            "type": "expense",
            "payment_method": "cash",
            "account_id": account_id,
            "category_id": category_id,
            "description": "Transaction for items list",
        },
    )
    assert r_tx.status_code == 201, r_tx.text
    transaction_id = r_tx.json()["id"]

    r_item = client.post(
        f"/api/transactions/{transaction_id}/items",
        json={
            "name": "Lunch",
            "amount": 25000,
            "unit_price": 25000,
        },
    )
    assert r_item.status_code == 201, r_item.text

    r = client.get(f"/api/transactions/{transaction_id}/items")
    assert r.status_code == 200, r.text
    data = r.json()
    assert isinstance(data, list)
    assert len(data) >= 1


def test_list_items_by_transaction_returns_404_for_missing_transaction(auth_client):
    fake_transaction_id = uuid.uuid4()
    r = auth_client.get(f"/api/transactions/{fake_transaction_id}/items")
    assert r.status_code == 404
    assert "detail" in r.json()


def test_create_item_for_transaction_returns_201_with_valid_data(auth_client_with_account):
    client, account_id, category_id = auth_client_with_account

    r_tx = client.post(
        "/api/transactions",
        json={
            "date": "2026-01-20",
            "amount": 80000,
            "type": "expense",
            "payment_method": "cash",
            "account_id": account_id,
            "category_id": category_id,
            "description": "Transaction for item creation",
        },
    )
    assert r_tx.status_code == 201, r_tx.text
    transaction_id = r_tx.json()["id"]

    r = client.post(
        f"/api/transactions/{transaction_id}/items",
        json={
            "name": "Lunch",
            "amount": 25000,
            "unit_price": 25000,
        },
    )
    assert r.status_code == 201, r.text
    data = r.json()
    assert data["name"] == "Lunch"
    # El API solo devuelve unit_price, así que validamos ese campo
    assert str(data["unit_price"]) in ("25000", "25000.00")


def test_create_item_for_transaction_returns_404_for_missing_transaction(auth_client):
    fake_transaction_id = uuid.uuid4()
    r = auth_client.post(
        f"/api/transactions/{fake_transaction_id}/items",
        json={
            "name": "Missing transaction item",
            "amount": 1000,
            "unit_price": 1000,
        },
    )
    assert r.status_code == 404, r.text
    assert "detail" in r.json()


def test_create_item_for_transaction_returns_422_with_invalid_data(auth_client_with_account):
    client, account_id, category_id = auth_client_with_account

    r_tx = client.post(
        "/api/transactions",
        json={
            "date": "2026-01-21",
            "amount": 30000,
            "type": "expense",
            "payment_method": "cash",
            "account_id": account_id,
            "category_id": category_id,
            "description": "Transaction for invalid item payload",
        },
    )
    assert r_tx.status_code == 201, r_tx.text
    transaction_id = r_tx.json()["id"]

    r = client.post(f"/api/transactions/{transaction_id}/items", json={})
    assert r.status_code == 422, r.text


def test_update_item_returns_501_or_404(auth_client):
    fake_item_id = uuid.uuid4()
    r = auth_client.patch(
        f"/api/items/{fake_item_id}",
        json={"name": "Updated item"},
    )
    assert r.status_code in (404, 501)


def test_list_items_by_transaction_without_auth_returns_401_403_or_404(client):
    fake_transaction_id = uuid.uuid4()
    r = client.get(f"/api/transactions/{fake_transaction_id}/items")
    assert r.status_code in (401, 403, 404)


def test_create_item_for_transaction_without_auth_returns_401_403_or_404(client):
    fake_transaction_id = uuid.uuid4()
    r = client.post(
        f"/api/transactions/{fake_transaction_id}/items",
        json={
            "name": "Unauthorized item",
            "amount": 1000,
            "unit_price": 1000,
        },
    )
    assert r.status_code in (401, 403, 404)


def test_update_item_without_auth_returns_401_403_404_or_501(client):
    fake_item_id = uuid.uuid4()
    r = client.patch(
        f"/api/items/{fake_item_id}",
        json={"name": "Unauthorized update"},
    )
    assert r.status_code in (401, 403, 404, 501)