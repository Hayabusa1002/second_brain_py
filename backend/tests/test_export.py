def test_export_json_returns_200_and_json_list(auth_client_with_account):
    # Create one transaction and export it as JSON
    client, account_id, category_id = auth_client_with_account

    client.post(
        "/api/transactions",
        json={
            "date": "2026-01-15",
            "amount": 50000,
            "type": "expense",
            "account_id": account_id,
            "category_id": category_id,
        },
    )

    r = client.get("/api/export/json")
    assert r.status_code == 200
    assert "application/json" in r.headers["content-type"]
    assert 'filename=transactions.json' in r.headers["content-disposition"]

    data = r.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert data[0]["type"] in ("income", "expense")


def test_export_json_with_type_filter_returns_filtered_results(auth_client_with_account):
    # Create one expense transaction and filter export by type
    client, account_id, category_id = auth_client_with_account

    client.post(
        "/api/transactions",
        json={
            "date": "2026-01-15",
            "amount": 50000,
            "type": "expense",
            "account_id": account_id,
            "category_id": category_id,
            "description": "Groceries",
        },
    )

    r = client.get("/api/export/json?type=expense")
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list)
    assert all(item["type"] == "expense" for item in data)


def test_export_json_with_search_filter_returns_matching_results(auth_client_with_account):
    # Create one transaction and filter export by description text
    client, account_id, category_id = auth_client_with_account

    client.post(
        "/api/transactions",
        json={
            "date": "2026-01-16",
            "amount": 15000,
            "type": "expense",
            "account_id": account_id,
            "category_id": category_id,
            "description": "Supermarket purchase",
        },
    )

    r = client.get("/api/export/json?q=Supermarket")
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert any("Supermarket" in (item.get("description") or "") for item in data)


def test_export_csv_returns_200_and_csv_content(auth_client_with_account):
    # Export should return CSV content with expected content type and filename
    client, _, _ = auth_client_with_account

    r = client.get("/api/export/csv")
    assert r.status_code == 200
    assert "text/csv" in r.headers["content-type"]
    assert 'filename=transactions.csv' in r.headers["content-disposition"]
    assert "date" in r.text


def test_export_xlsx_returns_200_and_binary_content(auth_client_with_account):
    # Export should return a non-empty XLSX file
    client, _, _ = auth_client_with_account

    r = client.get("/api/export/xlsx")
    assert r.status_code == 200
    assert "spreadsheetml" in r.headers["content-type"]
    assert 'filename=transactions.xlsx' in r.headers["content-disposition"]
    assert len(r.content) > 0


def test_export_pdf_returns_200_and_pdf_signature(auth_client_with_account):
    # Export should return a valid PDF file signature
    client, _, _ = auth_client_with_account

    r = client.get("/api/export/pdf")
    assert r.status_code == 200
    assert r.headers["content-type"] == "application/pdf"
    assert 'filename=transactions.pdf' in r.headers["content-disposition"]
    assert r.content[:4] == b"%PDF"


def test_export_endpoints_without_auth_return_401_or_403(client):
    # Anonymous users should not be able to export data
    for fmt in ["json", "csv", "xlsx", "pdf"]:
        r = client.get(f"/api/export/{fmt}")
        assert r.status_code in (401, 403)


def test_export_json_with_date_filter_returns_200(auth_client_with_account):
    # Export with date filters should return a valid response
    client, account_id, category_id = auth_client_with_account

    client.post(
        "/api/transactions",
        json={
            "date": "2026-01-20",
            "amount": 100000,
            "type": "income",
            "account_id": account_id,
            "category_id": category_id,
            "description": "Salary payment",
        },
    )

    r = client.get("/api/export/json?date_from=2026-01-01&date_to=2026-01-31")
    assert r.status_code == 200
    assert "application/json" in r.headers["content-type"]
    data = r.json()
    assert isinstance(data, list)


def test_export_json_with_account_filter_returns_matching_results(auth_client_with_account):
    # Export filtered by account_id should return a valid JSON list
    client, account_id, category_id = auth_client_with_account

    client.post(
        "/api/transactions",
        json={
            "date": "2026-01-21",
            "amount": 25000,
            "type": "expense",
            "account_id": account_id,
            "category_id": category_id,
            "description": "Taxi",
        },
    )

    r = client.get(f"/api/export/json?account_id={account_id}")
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list)
    assert len(data) >= 1