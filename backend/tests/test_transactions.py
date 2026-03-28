def test_create_transaction(auth_client_with_account):
    client, account_id, category_id = auth_client_with_account
    r = client.post("/api/transactions", json={
        "date":        "2026-01-15",
        "amount":      50000,
        "type":        "expense",
        "account_id":  account_id,
        "category_id": category_id,
        "description": "Test transaction",
    })
    assert r.status_code == 200
    data = r.json()
    assert data["amount"] == "50000"
    assert data["type"]   == "expense"

def test_list_transactions(auth_client_with_account):
    client, account_id, category_id = auth_client_with_account
    client.post("/api/transactions", json={
        "date": "2026-01-16", "amount": 2000000, "type": "income",
        "account_id": account_id, "category_id": category_id,
    })
    r = client.get("/api/transactions")
    assert r.status_code == 200
    assert len(r.json()) >= 1

def test_filter_transactions_by_type(auth_client_with_account):
    client, account_id, category_id = auth_client_with_account
    client.post("/api/transactions", json={
        "date": "2026-02-01", "amount": 10000, "type": "income",
        "account_id": account_id, "category_id": category_id,
    })
    r = client.get("/api/transactions?type=income")
    assert r.status_code == 200
    assert all(t["type"] == "income" for t in r.json())

def test_delete_transaction(auth_client_with_account):
    client, account_id, category_id = auth_client_with_account
    r = client.post("/api/transactions", json={
        "date": "2026-03-01", "amount": 5000, "type": "expense",
        "account_id": account_id, "category_id": category_id,
    })
    tx_id = r.json()["id"]
    r_del = client.delete(f"/api/transactions/{tx_id}")
    assert r_del.status_code == 200

def test_transaction_invalid_type(auth_client_with_account):
    client, account_id, category_id = auth_client_with_account
    r = client.post("/api/transactions", json={
        "date": "2026-03-01", "amount": 5000, "type": "invalid",
        "account_id": account_id, "category_id": category_id,
    })
    assert r.status_code == 422