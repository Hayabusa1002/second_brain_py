import io
import uuid


def test_create_transaction_with_valid_data_returns_201(auth_client_with_account):
    client, account_id, category_id = auth_client_with_account
    r = client.post(
        "/api/transactions",
        json={
            "date": "2026-01-15",
            "amount": 50000,
            "type": "expense",
            "payment_method": "cash",
            "account_id": account_id,
            "category_id": category_id,
            "description": "Test transaction",
        },
    )
    assert r.status_code == 201, r.text
    data = r.json()
    assert data["type"] == "expense"
    assert data["account_id"] == account_id
    assert data["category_id"] == category_id
    assert data["payment_method"] == "cash"


def test_list_transactions_returns_list(auth_client_with_account):
    client, account_id, category_id = auth_client_with_account
    client.post(
        "/api/transactions",
        json={
            "date": "2026-01-16",
            "amount": 2000000,
            "type": "income",
            "payment_method": "cash",
            "account_id": account_id,
            "category_id": category_id,
        },
    )
    r = client.get("/api/transactions")
    assert r.status_code == 200
    body = r.json()
    assert isinstance(body, dict)
    assert "items" in body
    assert "total" in body
    assert isinstance(body["items"], list)
    assert body["total"] >= 1
    assert len(body["items"]) >= 1


def test_filter_transactions_by_type_income_only(auth_client_with_account):
    client, account_id, category_id = auth_client_with_account

    client.post(
        "/api/transactions",
        json={
            "date": "2026-02-01",
            "amount": 10000,
            "type": "income",
            "payment_method": "cash",
            "account_id": account_id,
            "category_id": category_id,
        },
    )

    r = client.get("/api/transactions?type=income")
    assert r.status_code == 200
    body = r.json()
    items = body["items"]
    assert len(items) >= 1
    assert all(t["type"] == "income" for t in items)


def test_filter_transactions_by_date_range_returns_200(auth_client_with_account):
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
    body = r.json()
    assert isinstance(body, dict)
    assert isinstance(body["items"], list)


def test_get_transaction_by_id_returns_200(auth_client_with_account):
    client, account_id, category_id = auth_client_with_account
    r_create = client.post(
        "/api/transactions",
        json={
            "date": "2026-04-01",
            "amount": 12345,
            "type": "expense",
            "payment_method": "cash",
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
    assert data["amount"] == "12345.00"


def test_get_transaction_by_id_returns_404_for_missing_transaction(auth_client_with_account):
    client, _, _ = auth_client_with_account
    fake_id = uuid.uuid4()
    r = client.get(f"/api/transactions/{fake_id}")
    assert r.status_code == 404


def test_update_transaction_with_valid_data_returns_200(auth_client_with_account):
    client, account_id, category_id = auth_client_with_account
    r_create = client.post(
        "/api/transactions",
        json={
            "date": "2026-05-01",
            "amount": 10000,
            "type": "expense",
            "payment_method": "cash",
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
    client, _, _ = auth_client_with_account
    fake_id = uuid.uuid4()

    r = client.patch(
        "/api/transactions/{id}".replace("{id}", str(fake_id)),
        json={"description": "Does not matter"},
    )
    assert r.status_code == 404


def test_delete_transaction_returns_204(auth_client_with_account):
    client, account_id, category_id = auth_client_with_account
    r_create = client.post(
        "/api/transactions",
        json={
            "date": "2026-03-01",
            "amount": 5000,
            "type": "expense",
            "payment_method": "cash",
            "account_id": account_id,
            "category_id": category_id,
        },
    )
    assert r_create.status_code == 201
    tx_id = r_create.json()["id"]

    r_del = client.delete(f"/api/transactions/{tx_id}")
    assert r_del.status_code == 204


def test_delete_transaction_returns_404_for_missing_transaction(auth_client_with_account):
    client, _, _ = auth_client_with_account
    fake_id = uuid.uuid4()
    r_del = client.delete(f"/api/transactions/{fake_id}")
    assert r_del.status_code == 404


def test_create_transaction_with_invalid_type_returns_422(auth_client_with_account):
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
    r = auth_client.get("/api/transactions/import/template")
    assert r.status_code == 200
    assert "text/csv" in r.headers["content-type"]
    assert "import_template.csv" in r.headers["content-disposition"]
    assert "date,amount,type" in r.text


def test_import_transactions_with_unsupported_extension_returns_400(auth_client):
    fake_content = b"not,a,csv"
    file_obj = io.BytesIO(fake_content)
    r = auth_client.post(
        "/api/transactions/import",
        files={"file": ("data.txt", file_obj, "text/plain")},
    )
    assert r.status_code == 400
    assert r.json()["detail"] == "Unsupported format. Use .csv or .xlsx"


def test_list_items_returns_404_for_missing_transaction(auth_client_with_account):
    client, _, _ = auth_client_with_account
    fake_tx_id = uuid.uuid4()
    r = client.get(f"/api/transactions/{fake_tx_id}/items")
    assert r.status_code == 404


def test_create_item_for_missing_transaction_returns_404(auth_client_with_account):
    client, _, _ = auth_client_with_account
    fake_tx_id = uuid.uuid4()
    r = client.post(
        f"/api/transactions/{fake_tx_id}/items",
        json={
            "name": "Item",
            "amount": 1000,
            "unit_price": 1000,
        },
    )
    assert r.status_code == 404, r.text


def test_transactions_endpoints_without_auth_return_401_or_403(client):
    r = client.get("/api/transactions")
    assert r.status_code in (401, 403)