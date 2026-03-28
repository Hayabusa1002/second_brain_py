def test_create_account(auth_client):
    r = auth_client.post("/api/accounts", json={"name": "Nequi", "type": "individual"})
    assert r.status_code == 200
    assert r.json()["name"] == "Nequi"

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
    account_id = r.json()["id"]
    r_del = auth_client.delete(f"/api/accounts/{account_id}")
    assert r_del.status_code == 200