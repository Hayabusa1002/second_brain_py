from uuid import UUID


def test_list_items_returns_200(auth_client_with_account):
    client, _, _ = auth_client_with_account

    r = client.get("/api/items")
    assert r.status_code == 200, r.text
    assert isinstance(r.json(), list)


def test_get_item_returns_404_for_missing_item(auth_client_with_account):
    client, _, _ = auth_client_with_account

    r = client.get(f"/api/items/{UUID(int=0)}")
    assert r.status_code == 404, r.text


def test_create_item_returns_201_with_valid_data(auth_client_with_account):
    client, _, _ = auth_client_with_account

    r = client.post(
        "/api/items",
        json={
            "name": "Lunch",
            "subcategory_id": None,
        },
    )
    assert r.status_code == 201, r.text

    body = r.json()
    assert body["name"] == "Lunch"
    assert "id" in body


def test_create_item_returns_422_with_invalid_data(auth_client_with_account):
    client, _, _ = auth_client_with_account

    r = client.post("/api/items", json={})
    assert r.status_code == 422, r.text


def test_update_item_returns_404_for_missing_item(auth_client_with_account):
    client, _, _ = auth_client_with_account

    r = client.patch(
        f"/api/items/{UUID(int=0)}",
        json={"name": "Updated name"},
    )
    assert r.status_code == 404, r.text


def test_update_item_returns_200_with_valid_data(auth_client_with_account):
    client, _, _ = auth_client_with_account

    r_create = client.post(
        "/api/items",
        json={
            "name": "Lunch for update",
            "subcategory_id": None,
        },
    )
    assert r_create.status_code == 201, r_create.text
    item_id = r_create.json()["id"]

    r = client.patch(
        f"/api/items/{item_id}",
        json={"name": "Dinner"},
    )
    assert r.status_code == 200, r.text
    assert r.json()["name"] == "Dinner"


def test_list_items_without_auth_returns_401_or_403(client):
    r = client.get("/api/items")
    assert r.status_code in (401, 403), r.text


def test_create_item_without_auth_returns_401_or_403(client):
    r = client.post(
        "/api/items",
        json={
            "name": "Lunch",
            "subcategory_id": None,
        },
    )
    assert r.status_code in (401, 403), r.text


def test_update_item_without_auth_returns_401_or_403_or_404(client):
    r = client.patch(
        f"/api/items/{UUID(int=0)}",
        json={"name": "Dinner"},
    )
    assert r.status_code in (401, 403, 404), r.text