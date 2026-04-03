import uuid


def test_list_stores_returns_list(auth_client):
    # Should return a list of stores for an authorized admin user
    r = auth_client.get("/api/stores/")
    assert r.status_code == 200
    assert isinstance(r.json(), list)


def test_create_store_with_valid_data_returns_201(auth_client):
    # Should create a store successfully
    r = auth_client.post("/api/stores/", json={"name": "Exito"})
    assert r.status_code == 201
    data = r.json()
    assert data["name"] == "Exito"


def test_get_store_by_id_returns_200_for_existing_store(auth_client):
    # Should return an existing store by id
    r_create = auth_client.post("/api/stores/", json={"name": "Carulla"})
    assert r_create.status_code == 201
    store_id = r_create.json()["id"]

    r = auth_client.get(f"/api/stores/{store_id}")
    assert r.status_code == 200
    data = r.json()
    assert data["id"] == store_id
    assert data["name"] == "Carulla"


def test_get_store_by_id_returns_404_for_missing_store(auth_client):
    # Non-existing store id should return 404
    fake_id = uuid.uuid4()
    r = auth_client.get(f"/api/stores/{fake_id}")
    assert r.status_code == 404
    assert r.json()["detail"] == "Store not found"


def test_update_store_with_valid_data_returns_200(auth_client):
    # Should update an existing store
    r_create = auth_client.post("/api/stores/", json={"name": "Jumbo"})
    assert r_create.status_code == 201
    store_id = r_create.json()["id"]

    r = auth_client.patch(
        f"/api/stores/{store_id}",
        json={"name": "Jumbo Premium"},
    )
    assert r.status_code == 200
    data = r.json()
    assert data["id"] == store_id
    assert data["name"] == "Jumbo Premium"


def test_update_store_returns_404_for_missing_store(auth_client):
    # Updating a non-existing store should return 404
    fake_id = uuid.uuid4()
    r = auth_client.patch(
        f"/api/stores/{fake_id}",
        json={"name": "Unknown Store"},
    )
    assert r.status_code == 404
    assert r.json()["detail"] == "Store not found"


def test_create_store_without_name_returns_422(auth_client):
    # Missing required name should fail validation
    r = auth_client.post("/api/stores/", json={})
    assert r.status_code == 422


def test_create_store_without_auth_returns_401_or_403(client):
    # Anonymous user should not be able to create a store
    r = client.post("/api/stores/", json={"name": "D1"})
    assert r.status_code in (401, 403)


def test_list_stores_without_auth_returns_401_or_403(client):
    # Anonymous user should not be able to list stores
    r = client.get("/api/stores/")
    assert r.status_code in (401, 403)


def test_update_store_without_auth_returns_401_or_403(client):
    # Anonymous user should not be able to update a store
    fake_id = uuid.uuid4()
    r = client.patch(
        f"/api/stores/{fake_id}",
        json={"name": "No Auth Store"},
    )
    assert r.status_code in (401, 403)