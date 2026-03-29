def test_create_category(auth_client):
    r = auth_client.post("/api/categories", json={"name": "Arriendo", "type": "expense"})
    assert r.status_code == 201
    assert r.json()["name"] == "Arriendo"


def test_list_categories(auth_client):
    auth_client.post("/api/categories", json={"name": "Comida", "type": "expense"})
    r = auth_client.get("/api/categories")
    assert r.status_code == 200
    assert isinstance(r.json(), list)


def test_create_category_invalid_type(auth_client):
    r = auth_client.post("/api/categories", json={"name": "X", "type": "invalid"})
    assert r.status_code == 422


def test_category_name_required(auth_client):
    r = auth_client.post("/api/categories", json={"type": "expense"})
    assert r.status_code == 422