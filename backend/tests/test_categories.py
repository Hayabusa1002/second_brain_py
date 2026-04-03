import uuid


def test_create_category_with_valid_data_returns_201(auth_client):
    # Should create a category successfully
    r = auth_client.post("/api/categories", json={"name": "Rent", "type": "expense"})
    assert r.status_code == 201
    data = r.json()
    assert data["name"] == "Rent"
    assert data["type"] == "expense"


def test_list_categories_returns_list(auth_client):
    # Should return a list of categories
    auth_client.post("/api/categories", json={"name": "Food", "type": "expense"})
    r = auth_client.get("/api/categories")
    assert r.status_code == 200
    assert isinstance(r.json(), list)


def test_get_category_by_id_returns_200_for_existing_category(auth_client):
    # Should return an existing category by id
    r_create = auth_client.post("/api/categories", json={"name": "Salary", "type": "income"})
    assert r_create.status_code == 201
    category_id = r_create.json()["id"]

    r = auth_client.get(f"/api/categories/{category_id}")
    assert r.status_code == 200
    data = r.json()
    assert data["id"] == category_id
    assert data["name"] == "Salary"
    assert data["type"] == "income"


def test_get_category_by_id_returns_404_for_missing_category(auth_client):
    # Non-existing category id should return 404
    fake_id = uuid.uuid4()
    r = auth_client.get(f"/api/categories/{fake_id}")
    assert r.status_code == 404
    assert r.json()["detail"] == "Category not found"


def test_create_category_with_invalid_type_returns_422(auth_client):
    # Invalid enum/type value should fail validation
    r = auth_client.post("/api/categories", json={"name": "Invalid", "type": "invalid"})
    assert r.status_code == 422


def test_create_category_without_name_returns_422(auth_client):
    # Missing required name should fail validation
    r = auth_client.post("/api/categories", json={"type": "expense"})
    assert r.status_code == 422


def test_update_category_with_valid_data_returns_200(auth_client):
    # Should update an existing category
    r_create = auth_client.post("/api/categories", json={"name": "Transport", "type": "expense"})
    assert r_create.status_code == 201
    category_id = r_create.json()["id"]

    r = auth_client.patch(
        f"/api/categories/{category_id}",
        json={"name": "Public Transport", "type": "expense"},
    )
    assert r.status_code == 200
    data = r.json()
    assert data["id"] == category_id
    assert data["name"] == "Public Transport"
    assert data["type"] == "expense"


def test_update_category_with_partial_data_returns_200(auth_client):
    # Should allow partial update if CategoryUpdate supports optional fields
    r_create = auth_client.post("/api/categories", json={"name": "Utilities", "type": "expense"})
    assert r_create.status_code == 201
    category_id = r_create.json()["id"]

    r = auth_client.patch(
        f"/api/categories/{category_id}",
        json={"name": "Home Utilities"},
    )
    assert r.status_code == 200
    data = r.json()
    assert data["id"] == category_id
    assert data["name"] == "Home Utilities"


def test_update_category_returns_404_for_missing_category(auth_client):
    # Updating a non-existing category should return 404
    fake_id = uuid.uuid4()
    r = auth_client.patch(
        f"/api/categories/{fake_id}",
        json={"name": "Anything", "type": "expense"},
    )
    assert r.status_code == 404
    assert r.json()["detail"] == "Category not found"


def test_create_category_without_auth_returns_401_or_403(client):
    # Protected endpoint should reject anonymous requests
    r = client.post("/api/categories", json={"name": "Rent", "type": "expense"})
    assert r.status_code in (401, 403)


def test_update_category_without_auth_returns_401_or_403(client):
    # Protected update endpoint should reject anonymous requests
    fake_id = uuid.uuid4()
    r = client.patch(
        f"/api/categories/{fake_id}",
        json={"name": "NoAuth", "type": "expense"},
    )
    assert r.status_code in (401, 403)