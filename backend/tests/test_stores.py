import uuid


def test_list_stores_returns_list(admin_client):
    r = admin_client.get("/api/stores/")
    assert r.status_code == 200
    assert isinstance(r.json(), list)


def test_create_store_with_valid_data_returns_201(admin_client):
    r = admin_client.post(
        "/api/stores/",
        json={"name": "Exito", "type": "physical"},
    )
    assert r.status_code == 201
    data = r.json()
    assert data["name"] == "Exito"
    assert data["type"] == "physical"


def test_get_store_by_id_returns_200_for_existing_store(admin_client):
    r_create = admin_client.post(
        "/api/stores/",
        json={"name": "Carulla", "type": "physical"},
    )
    assert r_create.status_code == 201
    store_id = r_create.json()["id"]

    r = admin_client.get(f"/api/stores/{store_id}")
    assert r.status_code == 200
    data = r.json()
    assert data["id"] == store_id
    assert data["name"] == "Carulla"
    assert data["type"] == "physical"


def test_get_store_by_id_returns_404_for_missing_store(admin_client):
    fake_id = uuid.uuid4()
    r = admin_client.get(f"/api/stores/{fake_id}")
    assert r.status_code == 404


def test_update_store_with_valid_data_returns_200(admin_client):
    r_create = admin_client.post(
        "/api/stores/",
        json={"name": "Jumbo", "type": "physical"},
    )
    assert r_create.status_code == 201
    store_id = r_create.json()["id"]

    r = admin_client.patch(
        f"/api/stores/{store_id}",
        json={"name": "Jumbo Premium"},
    )
    assert r.status_code == 200
    data = r.json()
    assert data["id"] == store_id
    assert data["name"] == "Jumbo Premium"


def test_update_store_returns_404_for_missing_store(admin_client):
    fake_id = uuid.uuid4()
    r = admin_client.patch(
        f"/api/stores/{fake_id}",
        json={"name": "Unknown Store"},
    )
    assert r.status_code == 404


def test_create_store_without_name_returns_422(admin_client):
    r = admin_client.post("/api/stores/", json={})
    assert r.status_code == 422


def test_create_store_without_auth_returns_401_or_403(client):
    r = client.post(
        "/api/stores/",
        json={"name": "D1", "type": "physical"},
    )
    assert r.status_code in (401, 403)


def test_list_stores_without_auth_returns_401_or_403(client):
    r = client.get("/api/stores/")
    assert r.status_code in (401, 403)


def test_update_store_without_auth_returns_401_or_403(client):
    fake_id = uuid.uuid4()
    r = client.patch(
        f"/api/stores/{fake_id}",
        json={"name": "No Auth Store"},
    )
    assert r.status_code in (401, 403)