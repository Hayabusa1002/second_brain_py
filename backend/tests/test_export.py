def test_export_json(auth_client_with_account):
    client, account_id, category_id = auth_client_with_account
    client.post("/api/transactions", json={
        "date": "2026-01-15", "amount": 50000, "type": "expense",
        "account_id": account_id, "category_id": category_id,
    })
    r = client.get("/api/export/json")
    assert r.status_code == 200
    assert "application/json" in r.headers["content-type"]
    data = r.json()
    assert isinstance(data, list)
    assert data[0]["type"] in ("income", "expense")


def test_export_csv(auth_client_with_account):
    client, _, __ = auth_client_with_account
    r = client.get("/api/export/csv")
    assert r.status_code == 200
    assert "text/csv" in r.headers["content-type"]
    assert "date" in r.text


def test_export_xlsx(auth_client_with_account):
    client, _, __ = auth_client_with_account
    r = client.get("/api/export/xlsx")
    assert r.status_code == 200
    assert "spreadsheetml" in r.headers["content-type"]
    assert len(r.content) > 0


def test_export_pdf(auth_client_with_account):
    client, _, __ = auth_client_with_account
    r = client.get("/api/export/pdf")
    assert r.status_code == 200
    assert r.headers["content-type"] == "application/pdf"
    assert r.content[:4] == b"%PDF"


def test_export_without_auth(client):
    for fmt in ["json", "csv", "xlsx", "pdf"]:
        r = client.get(f"/api/export/{fmt}")
        assert r.status_code in (401, 403)