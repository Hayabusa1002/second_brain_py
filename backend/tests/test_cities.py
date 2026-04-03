import uuid


def test_list_cities_returns_list(admin_client):
    r = admin_client.get("/api/cities/")
    assert r.status_code == 200
    assert isinstance(r.json(), list)


def test_create_city_with_valid_data_returns_201(admin_client):
    r = admin_client.post("/api/cities/", json={"name": "Medellin"})
    assert r.status_code == 201
    data = r.json()
    assert data["name"] == "Medellin"


def test_get_city_by_id_returns_200_for_existing_city(admin_client):
    r_create = admin_client.post("/api/cities/", json={"name": "Bogota"})
    assert r_create.status_code == 201
    city_id = r_create.json()["id"]

    r = admin_client.get(f"/api/cities/{city_id}")
    assert r.status_code == 200
    data = r.json()
    assert data["id"] == city_id
    assert data["name"] == "Bogota"


def test_get_city_by_id_returns_404_for_missing_city(admin_client):
    fake_id = uuid.uuid4()
    r = admin_client.get(f"/api/cities/{fake_id}")
    assert r.status_code == 404


def test_update_city_with_valid_data_returns_200(admin_client):
    r_create = admin_client.post("/api/cities/", json={"name": "Cali"})
    assert r_create.status_code == 201
    city_id = r_create.json()["id"]

    r = admin_client.patch(
        f"/api/cities/{city_id}",
        json={"name": "Santiago de Cali"},
    )
    assert r.status_code == 200
    data = r.json()
    assert data["id"] == city_id
    assert data["name"] == "Santiago de Cali"


def test_update_city_returns_404_for_missing_city(admin_client):
    fake_id = uuid.uuid4()
    r = admin_client.patch(
        f"/api/cities/{fake_id}",
        json={"name": "Unknown City"},
    )
    assert r.status_code == 404


def test_create_city_without_name_returns_422(admin_client):
    r = admin_client.post("/api/cities/", json={})
    assert r.status_code == 422


def test_create_city_without_auth_returns_401_or_403(client):
    r = client.post("/api/cities/", json={"name": "Barranquilla"})
    assert r.status_code in (401, 403)


def test_list_cities_without_auth_returns_401_or_403(client):
    r = client.get("/api/cities/")
    assert r.status_code in (401, 403)


def test_update_city_without_auth_returns_401_or_403(client):
    fake_id = uuid.uuid4()
    r = client.patch(
        f"/api/cities/{fake_id}",
        json={"name": "No Auth City"},
    )
    assert r.status_code in (401, 403)