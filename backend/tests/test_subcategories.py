import uuid


def test_list_subcategories_returns_list(admin_client):
    # Should return a list of subcategories for an authorized admin user
    r = admin_client.get("/api/subcategories/")
    assert r.status_code == 200, r.text
    assert isinstance(r.json(), list)


def test_create_subcategory_with_valid_data_returns_201(admin_client):
    # Should create a subcategory successfully when category exists
    r_category = admin_client.post(
        "/api/categories",
        json={"name": "Food", "type": "expense"},
    )
    assert r_category.status_code == 201, r_category.text
    category_id = r_category.json()["id"]

    r = admin_client.post(
        "/api/subcategories/",
        json={
            "name": "Restaurant",
            "category_id": category_id,
        },
    )
    assert r.status_code == 201, r.text
    data = r.json()
    assert data["name"] == "Restaurant"
    assert data["category_id"] == category_id


def test_list_subcategories_with_category_filter_returns_filtered_results(admin_client):
    # Should filter subcategories by category_id
    r_category = admin_client.post(
        "/api/categories",
        json={"name": "Transport", "type": "expense"},
    )
    assert r_category.status_code == 201, r_category.text
    category_id = r_category.json()["id"]

    r_sub = admin_client.post(
        "/api/subcategories/",
        json={
            "name": "Bus",
            "category_id": category_id,
        },
    )
    assert r_sub.status_code == 201, r_sub.text

    r = admin_client.get(f"/api/subcategories/?category_id={category_id}")
    assert r.status_code == 200, r.text
    data = r.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert all(item["category_id"] == category_id for item in data)


def test_get_subcategory_by_id_returns_200_for_existing_subcategory(admin_client):
    # Should return an existing subcategory by id
    r_category = admin_client.post(
        "/api/categories",
        json={"name": "Entertainment", "type": "expense"},
    )
    assert r_category.status_code == 201, r_category.text
    category_id = r_category.json()["id"]

    r_create = admin_client.post(
        "/api/subcategories/",
        json={
            "name": "Cinema",
            "category_id": category_id,
        },
    )
    assert r_create.status_code == 201, r_create.text
    subcategory_id = r_create.json()["id"]

    r = admin_client.get(f"/api/subcategories/{subcategory_id}")
    assert r.status_code == 200, r.text
    data = r.json()
    assert data["id"] == subcategory_id
    assert data["name"] == "Cinema"


def test_get_subcategory_by_id_returns_404_for_missing_subcategory(admin_client):
    # Non-existing subcategory id should return 404
    fake_id = uuid.uuid4()
    r = admin_client.get(f"/api/subcategories/{fake_id}")
    assert r.status_code == 404, r.text


def test_create_subcategory_returns_400_for_invalid_category(admin_client):
    # Creating a subcategory with a non-existing category should return 400
    fake_category_id = uuid.uuid4()

    r = admin_client.post(
        "/api/subcategories/",
        json={
            "name": "Invalid relation",
            "category_id": str(fake_category_id),
        },
    )
    assert r.status_code == 400, r.text


def test_create_subcategory_without_required_fields_returns_422(admin_client):
    # Missing required fields should fail validation
    r = admin_client.post("/api/subcategories/", json={})
    assert r.status_code == 422, r.text


def test_update_subcategory_with_valid_data_returns_200(admin_client):
    # Should update an existing subcategory
    r_category = admin_client.post(
        "/api/categories",
        json={"name": "Health", "type": "expense"},
    )
    assert r_category.status_code == 201, r_category.text
    category_id = r_category.json()["id"]

    r_create = admin_client.post(
        "/api/subcategories/",
        json={
            "name": "Medicine",
            "category_id": category_id,
        },
    )
    assert r_create.status_code == 201, r_create.text
    subcategory_id = r_create.json()["id"]

    r = admin_client.patch(
        f"/api/subcategories/{subcategory_id}",
        json={"name": "Pharmacy"},
    )
    assert r.status_code == 200, r.text
    data = r.json()
    assert data["id"] == subcategory_id
    assert data["name"] == "Pharmacy"


def test_update_subcategory_returns_404_for_missing_subcategory(admin_client):
    # Updating a non-existing subcategory should return 404
    fake_id = uuid.uuid4()
    r = admin_client.patch(
        f"/api/subcategories/{fake_id}",
        json={"name": "Unknown subcategory"},
    )
    assert r.status_code == 404, r.text


def test_list_subcategories_without_auth_returns_401_or_403(client):
    # Anonymous users should not be able to list subcategories
    r = client.get("/api/subcategories/")
    assert r.status_code in (401, 403)


def test_create_subcategory_without_auth_returns_401_or_403(client):
    # Anonymous users should not be able to create subcategories
    r = client.post(
        "/api/subcategories/",
        json={
            "name": "Unauthorized sub",
            "category_id": str(uuid.uuid4()),
        },
    )
    assert r.status_code in (401, 403)


def test_update_subcategory_without_auth_returns_401_or_403(client):
    # Anonymous users should not be able to update subcategories
    fake_id = uuid.uuid4()
    r = client.patch(
        f"/api/subcategories/{fake_id}",
        json={"name": "Unauthorized update"},
    )
    assert r.status_code in (401, 403)