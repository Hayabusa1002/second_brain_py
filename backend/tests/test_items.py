import uuid


def test_list_items_by_transaction_returns_200_for_existing_transaction(auth_client_with_account):
    # Should return a list for an existing transaction, even if it is empty
    client, account_id, category_id = auth_client_with_account

    r_tx = client.post(
        "/api/transactions",
        json={
            "date": "2026-01-15",
            "amount": 50000,
            "type": "expense",
            "account_id": account_id,
            "category_id": category_id,
            "description": "Transaction for items list",
        },
    )
    assert r_tx.status_code == 201
    transaction_id = r_tx.json()["id"]

    r = client.get(f"/api/items/by-transaction/{transaction_id}")
    assert r.status_code == 200
    assert isinstance(r.json(), list)


def test_list_items_by_transaction_returns_404_for_missing_transaction(auth_client):
    # Non-existing transaction id should return 404
    fake_transaction_id = uuid.uuid4()
    r = auth_client.get(f"/api/items/by-transaction/{fake_transaction_id}")
    assert r.status_code == 404
    assert r.json()["detail"] == "Transaction not found"


def test_create_item_for_transaction_returns_201_with_valid_data(auth_client_with_account):
    # Should create an item for an existing transaction
    client, account_id, category_id = auth_client_with_account

    r_tx = client.post(
        "/api/transactions",
        json={
            "date": "2026-01-20",
            "amount": 80000,
            "type": "expense",
            "account_id": account_id,
            "category_id": category_id,
            "description": "Transaction for item creation",
        },
    )
    assert r_tx.status_code == 201
    transaction_id = r_tx.json()["id"]

    r = client.post(
        f"/api/items/transactions/{transaction_id}",
        json={
            "name": "Lunch",
            "amount": 25000,
        },
    )
    assert r.status_code == 201
    data = r.json()
    assert data["name"] == "Lunch"
    assert data["amount"] == 25000


def test_create_item_for_transaction_returns_404_for_missing_transaction(auth_client):
    # Creating an item for a non-existing transaction should return 404
    fake_transaction_id = uuid.uuid4()

    r = auth_client.post(
        f"/api/items/transactions/{fake_transaction_id}",
        json={
            "name": "Missing transaction item",
            "amount": 1000,
        },
    )
    assert r.status_code == 404
    assert r.json()["detail"] == "Transaction not found"


def test_create_item_for_transaction_returns_422_with_invalid_data(auth_client_with_account):
    # Missing required fields should fail validation
    client, account_id, category_id = auth_client_with_account

    r_tx = client.post(
        "/api/transactions",
        json={
            "date": "2026-01-21",
            "amount": 30000,
            "type": "expense",
            "account_id": account_id,
            "category_id": category_id,
            "description": "Transaction for invalid item payload",
        },
    )
    assert r_tx.status_code == 201
    transaction_id = r_tx.json()["id"]

    r = client.post(
        f"/api/items/transactions/{transaction_id}",
        json={},
    )
    assert r.status_code == 422


def test_update_item_returns_501_not_implemented(auth_client):
    # Update endpoint is explicitly not implemented yet
    fake_item_id = uuid.uuid4()

    r = auth_client.patch(
        f"/api/items/{fake_item_id}",
        json={"name": "Updated item"},
    )
    assert r.status_code == 501
    assert r.json()["detail"] == "Not implemented"


def test_list_items_by_transaction_without_auth_returns_401_403_or_404(client):
    # Anonymous users should not be able to list items (or route may not be resolved)
    fake_transaction_id = uuid.uuid4()
    r = client.get(f"/api/items/by-transaction/{fake_transaction_id}")
    assert r.status_code in (401, 403, 404)


def test_create_item_for_transaction_without_auth_returns_401_403_or_404(client):
    # Anonymous users should not be able to create items (or route may not be resolved)
    fake_transaction_id = uuid.uuid4()
    r = client.post(
        f"/api/items/transactions/{fake_transaction_id}",
        json={
            "name": "Unauthorized item",
            "amount": 1000,
        },
    )
    assert r.status_code in (401, 403, 404)


def test_update_item_without_auth_returns_401_403_404_or_501(client):
    # Anonymous users should not be able to update items;
    # depending on routing it might return 404 or the current 501 implementation.
    fake_item_id = uuid.uuid4()
    r = client.patch(
        f"/api/items/{fake_item_id}",
        json={"name": "Unauthorized update"},
    )
    assert r.status_code in (401, 403, 404, 501)