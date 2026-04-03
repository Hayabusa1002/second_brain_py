import io
import uuid


def test_create_transaction_with_valid_data_returns_201(auth_client_with_account):
    # Should create a transaction successfully
    client, account_id, category_id = auth_client_with_account
    r = client.post(
        "/api/transactions",
        json={
            "date": "2026-01-15",
            "amount": 50000,
            "type": "expense",
            "account_id": account_id,
            "category_id": category_id,
            "description": "Test transaction",
        },
    )
    assert r.status_code == 201
    data = r.json()
    assert data["type"] == "expense"
    assert data["account_id"] == account_id
    assert data["category_id"] == category_id


def test_list_transactions_returns_list(auth_client_with_account):
    # Should return a list of transactions for the current user
    client, account_id, category_id = auth_client_with_account
    client.post(
        "/api/transactions",
        json={
            "date": "2026-01-16",
            "amount": 2000000,
            "type": "income",
            "account_id": account_id,
            "category_id": category_id,
        },
    )
    r = client.get("/api/transactions")
    assert r.status_code == 200
    assert isinstance(r.json(), list)
    assert len(r.json()) >= 1


def test_filter_transactions_by_type_income_only(auth_client_with_account):
    # Filter by type=income should only return income transactions
    client, account_id, category_id = auth_client_with_account

    client.post(
        "/api/transactions",
        json={
            "date": "2026-02-01",
            "amount": 10000,
            "type": "income",
            "account_id": account_id,
            "category_id": category_id,
        },
    )

    r = client.get("/api/transactions?type=income")
    assert r.status_code == 200
    data = r.json()
    assert len(data) >= 1
    assert all(t["type"] == "income" for t in data)


def test_filter_transactions_by_date_range_returns_200(auth_client_with_account):
    # Date range filters should return a valid response
    client, account_id, category_id = auth_client_with_account

    client.post(
        "/api/transactions",
        json={
            "date": "2026-03-10",
            "amount": 70000,
            "type": "expense",
            "account_id": account_id,
            "category_id": category_id,
            "description": "Groceries",
        },
    )

    r = client.get("/api/transactions?date_from=2026-03-01&date_to=2026-03-31")
    assert r.status_code == 200
    assert isinstance(r.json(), list)


def test_get_transaction_by_id_returns_200(auth_client_with_account):
    # Should return transaction detail for an existing id
    client, account_id, category_id = auth_client_with_account
    r_create = client.post(
        "/api/transactions",
        json={
            "date": "2026-04-01",
            "amount": 12345,
            "type": "expense",
            "account_id": account_id,
            "category_id": category_id,
            "description": "Detail test",
        },
    )
    assert r_create.status_code == 201
    tx_id = r_create.json()["id"]

    r = client.get(f"/api/transactions/{tx_id}")
    assert r.status_code == 200
    data = r.json()
    assert data["id"] == tx_id
    assert data["amount"] == 12345


def test_get_transaction_by_id_returns_404_for_missing_transaction(auth_client_with_account):
    # Non-existing transaction id should return 404
    client, _, _ = auth_client_with_account
    fake_id = uuid.uuid4()
    r = client.get(f"/api/transactions/{fake_id}")
    assert r.status_code == 404


def test_update_transaction_with_valid_data_returns_200(auth_client_with_account):
    # Should update an existing transaction
    client, account_id, category_id = auth_client_with_account
    r_create = client.post(
        "/api/transactions",
        json={
            "date": "2026-05-01",
            "amount": 10000,
            "type": "expense",
            "account_id": account_id,
            "category_id": category_id,
            "description": "Old description",
        },
    )
    assert r_create.status_code == 201
    tx_id = r_create.json()["id"]

    r = client.patch(
        f"/api/transactions/{tx_id}",
        json={"description": "Updated description"},
    )
    assert r.status_code == 200
    data = r.json()
    assert data["id"] == tx_id
    assert data["description"] == "Updated description"


def test_update_transaction_returns_404_for_missing_transaction(auth_client_with_account):
    # Updating non-existing transaction should return 404
    client, _, _ = auth_client_with_account
    fake_id = uuid.uuid4()

    r = client.patch(
        "/api/transactions/{id}".replace("{id}", str(fake_id)),
        json={"description": "Does not matter"},
    )
    assert r.status_code == 404


def test_delete_transaction_returns_204(auth_client_with_account):
    # Should delete an existing transaction
    client, account_id, category_id = auth_client_with_account
    r_create = client.post(
        "/api/transactions",
        json={
            "date": "2026-03-01",
            "amount": 5000,
            "type": "expense",
            "account_id": account_id,
            "category_id": category_id,
        },
    )
    assert r_create.status_code == 201
    tx_id = r_create.json()["id"]

    r_del = client.delete(f"/api/transactions/{tx_id}")
    assert r_del.status_code == 204


def test_delete_transaction_returns_404_for_missing_transaction(auth_client_with_account):
    # Deleting non-existing transaction should return 404
    client, _, _ = auth_client_with_account
    fake_id = uuid.uuid4()
    r_del = client.delete(f"/api/transactions/{fake_id}")
    assert r_del.status_code == 404


def test_create_transaction_with_invalid_type_returns_422(auth_client_with_account):
    # Invalid enum/type value should fail validation
    client, account_id, category_id = auth_client_with_account
    r = client.post(
        "/api/transactions",
        json={
            "date": "2026-03-01",
            "amount": 5000,
            "type": "invalid",
            "account_id": account_id,
            "category_id": category_id,
        },
    )
    assert r.status_code == 422


def test_download_import_template_returns_csv(auth_client):
    # Template endpoint should return CSV content as attachment
    r = auth_client.get("/api/transactions/import/template")
    assert r.status_code == 200
    assert "text/csv" in r.headers["content-type"]
    assert "import_template.csv" in r.headers["content-disposition"]
    assert "date,amount,type" in r.text


def test_import_transactions_with_unsupported_extension_returns_400(auth_client):
    # Uploading a file with unsupported extension should return 400
    fake_content = b"not,a,csv"
    file_obj = io.BytesIO(fake_content)
    r = auth_client.post(
        "/api/transactions/import",
        files={"file": ("data.txt", file_obj, "text/plain")},
    )
    assert r.status_code == 400
    assert r.json()["detail"] == "Unsupported format. Use .csv or .xlsx"


def test_list_items_returns_404_for_missing_transaction(auth_client_with_account):
    # Listing items for non-existing transaction should return 404
    client, _, _ = auth_client_with_account
    fake_tx_id = uuid.uuid4()
    r = client.get(f"/api/transactions/{fake_tx_id}/items")
    assert r.status_code == 404


def test_create_item_for_missing_transaction_returns_404(auth_client_with_account):
    # Creating item for non-existing transaction should return 404
    client, _, _ = auth_client_with_account
    fake_tx_id = uuid.uuid4()
    r = client.post(
        f"/api/transactions/{fake_tx_id}/items",
        json={"name": "Item", "amount": 1000},
    )
    assert r.status_code == 404


def test_transactions_endpoints_without_auth_return_401_or_403(client):
    # Anonymous users should not be able to access transactions list
    r = client.get("/api/transactions")
    assert r.status_code in (401, 403)