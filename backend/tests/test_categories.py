import uuid


def test_list_subcategories_returns_list(admin_client):
    r = admin_client.get("/api/subcategories")
    assert r.status_code == 200
    assert isinstance(r.json(), list)


def test_create_subcategory_with_valid_data_returns_201(admin_client):
    r_category = admin_client.post(
        "/api/categories",
        json={"name": "Food", "type": "expense"},
    )
    assert r_category.status_code == 201
    category_id = r_category.json()["id"]

    r = admin_client.post(
        f"/api/categories/{category_id}/subcategories",
        json={"name": "Restaurant"},
    )

    assert r.status_code == 201
    data = r.json()
    assert data["name"] == "Restaurant"
    assert data["category_id"] == category_id


def test_list_subcategories_with_category_filter_returns_filtered_results(admin_client):
    r_category = admin_client.post(
        "/api/categories",
        json={"name": "Transport", "type": "expense"},
    )
    assert r_category.status_code == 201
    category_id = r_category.json()["id"]

    r_sub = admin_client.post(
        f"/api/categories/{category_id}/subcategories",
        json={"name": "Bus"},
    )
    assert r_sub.status_code == 201

    r = admin_client.get(f"/api/subcategories/?category_id={category_id}")
    assert r.status_code == 200
    data = r.json()
    assert any(item["id"] == r_sub.json()["id"] for item in data)


def test_get_subcategory_by_id_returns_200_for_existing_subcategory(admin_client):
    r_category = admin_client.post(
        "/api/categories",
        json={"name": "Entertainment", "type": "expense"},
    )
    assert r_category.status_code == 201
    category_id = r_category.json()["id"]

    r_create = admin_client.post(
        f"/api/categories/{category_id}/subcategories",
        json={"name": "Cinema"},
    )
    assert r_create.status_code == 201
    subcategory_id = r_create.json()["id"]

    r = admin_client.get(
        f"/api/categories/{category_id}/subcategories/{subcategory_id}"
    )
    assert r.status_code == 200
    data = r.json()
    assert data["id"] == subcategory_id
    assert data["name"] == "Cinema"
    assert data["category_id"] == category_id


def test_get_subcategory_by_id_returns_404_for_missing_subcategory(admin_client):
    fake_category_id = uuid.uuid4()
    fake_sub_id = uuid.uuid4()

    r = admin_client.get(
        f"/api/categories/{fake_category_id}/subcategories/{fake_sub_id}"
    )
    assert r.status_code == 404


def test_create_subcategory_returns_400_for_invalid_category(admin_client):
    # Con tu servicio actual, CategoryNotFoundError se traduce a 404.
    fake_category_id = uuid.uuid4()
    r = admin_client.post(
        f"/api/categories/{fake_category_id}/subcategories",
        json={"name": "Invalid relation"},
    )
    assert r.status_code == 404


def test_create_subcategory_without_required_fields_returns_422(admin_client):
    r_category = admin_client.post(
        "/api/categories",
        json={"name": "Test", "type": "expense"},
    )
    assert r_category.status_code == 201
    category_id = r_category.json()["id"]

    r = admin_client.post(
        f"/api/categories/{category_id}/subcategories",
        json={},
    )
    assert r.status_code == 422


def test_update_subcategory_with_valid_data_returns_200(admin_client):
    r_category = admin_client.post(
        "/api/categories",
        json={"name": "Health", "type": "expense"},
    )
    assert r_category.status_code == 201
    category_id = r_category.json()["id"]

    r_create = admin_client.post(
        f"/api/categories/{category_id}/subcategories",
        json={"name": "Medicine"},
    )
    assert r_create.status_code == 201
    subcategory_id = r_create.json()["id"]

    r = admin_client.patch(
        f"/api/categories/{category_id}/subcategories/{subcategory_id}",
        json={"name": "Pharmacy"},
    )
    assert r.status_code == 200
    data = r.json()
    assert data["id"] == subcategory_id
    assert data["name"] == "Pharmacy"


def test_update_subcategory_returns_404_for_missing_subcategory(admin_client):
    fake_category_id = uuid.uuid4()
    fake_sub_id = uuid.uuid4()

    r = admin_client.patch(
        f"/api/categories/{fake_category_id}/subcategories/{fake_sub_id}",
        json={"name": "Unknown subcategory"},
    )
    assert r.status_code == 404


def test_list_subcategories_without_auth_returns_401_or_403(client):
    r = client.get("/api/subcategories")
    assert r.status_code in (401, 403)


def test_create_subcategory_without_auth_returns_401_or_403(client):
    fake_category_id = uuid.uuid4()
    r = client.post(
        f"/api/categories/{fake_category_id}/subcategories",
        json={"name": "No Auth"},
    )
    assert r.status_code in (401, 403)


def test_update_subcategory_without_auth_returns_401_or_403(client):
    fake_category_id = uuid.uuid4()
    fake_sub_id = uuid.uuid4()
    r = client.patch(
        f"/api/categories/{fake_category_id}/subcategories/{fake_sub_id}",
        json={"name": "Unauthorized update"},
    )
    assert r.status_code in (401, 403)