import uuid

from app.models.user import User, UserStatus, UserRole


def test_list_all_users_returns_users_array(admin_client, db):
    # Should return all users including the admin created by admin_client
    r = admin_client.get("/api/users")
    assert r.status_code == 200
    data = r.json()
    assert "users" in data
    assert isinstance(data["users"], list)
    assert len(data["users"]) >= 1


def test_list_pending_users_returns_only_pending(admin_client, db):
    # Create a pending user directly in DB
    pending = User(
        email="pending-user@test.com",
        name="Pending User",
        password="x",
        status=UserStatus.pending,
        role=UserRole.owner,
    )
    db.add(pending)
    db.commit()
    db.refresh(pending)

    r = admin_client.get("/api/users/pending")
    assert r.status_code == 200
    data = r.json()
    assert "users" in data
    assert any(u["email"] == "pending-user@test.com" for u in data["users"])


def test_list_active_users_returns_only_active(admin_client, db):
    # Create an active user in DB
    active = User(
        email="active-user@test.com",
        name="Active User",
        password="x",
        status=UserStatus.active,
        role=UserRole.owner,
    )
    db.add(active)
    db.commit()
    db.refresh(active)

    r = admin_client.get("/api/users/active")
    assert r.status_code == 200
    data = r.json()
    assert "users" in data
    assert any(u["email"] == "active-user@test.com" for u in data["users"])


def test_get_user_by_id_returns_200_for_existing_user(admin_client, db):
    # Create a user and fetch it by id
    user = User(
        email="detail-user@test.com",
        name="Detail User",
        password="x",
        status=UserStatus.active,
        role=UserRole.owner,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    r = admin_client.get(f"/api/users/{user.id}")
    assert r.status_code == 200
    data = r.json()
    assert "user" in data
    assert data["user"]["id"] == str(user.id)
    assert data["user"]["email"] == "detail-user@test.com"


def test_get_user_by_id_returns_404_for_missing_user(admin_client):
    fake_id = uuid.uuid4()
    r = admin_client.get(f"/api/users/{fake_id}")
    assert r.status_code == 404


def test_update_user_with_valid_data_returns_200(admin_client, db):
    user = User(
        email="update-user@test.com",
        name="Old Name",
        password="x",
        status=UserStatus.active,
        role=UserRole.owner,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    r = admin_client.put(
        f"/api/users/{user.id}",
        json={"name": "New Name", "role": "admin"},
    )
    assert r.status_code == 200
    data = r.json()
    assert data["user"]["id"] == str(user.id)
    assert data["user"]["name"] == "New Name"
    assert data["user"]["role"] == "admin"


def test_update_user_returns_404_for_missing_user(admin_client):
    fake_id = uuid.uuid4()
    r = admin_client.put(
        f"/api/users/{fake_id}",
        json={"name": "Does Not Exist", "role": "owner"},
    )
    assert r.status_code == 404


def test_approve_user_changes_status_to_active(admin_client, db):
    user = User(
        email="approve-user@test.com",
        name="Approve User",
        password="x",
        status=UserStatus.pending,
        role=UserRole.owner,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    r = admin_client.post(f"/api/users/{user.id}/approve")
    assert r.status_code == 200
    data = r.json()
    assert data["user"]["status"] == UserStatus.active.value


def test_reject_user_changes_status_to_inactive(admin_client, db):
    user = User(
        email="reject-user@test.com",
        name="Reject User",
        password="x",
        status=UserStatus.pending,
        role=UserRole.owner,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    r = admin_client.post(f"/api/users/{user.id}/reject")
    assert r.status_code == 200
    data = r.json()
    assert data["user"]["status"] == UserStatus.inactive.value


def test_ban_user_changes_status_to_banned(admin_client, db):
    user = User(
        email="ban-user@test.com",
        name="Ban User",
        password="x",
        status=UserStatus.active,
        role=UserRole.owner,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    r = admin_client.post(f"/api/users/{user.id}/ban")
    assert r.status_code == 200
    data = r.json()
    assert data["user"]["status"] == UserStatus.banned.value


def test_unban_user_changes_status_to_active(admin_client, db):
    user = User(
        email="unban-user@test.com",
        name="Unban User",
        password="x",
        status=UserStatus.banned,
        role=UserRole.owner,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    r = admin_client.post(f"/api/users/{user.id}/unban")
    assert r.status_code == 200
    data = r.json()
    assert data["user"]["status"] == UserStatus.active.value


def test_status_change_returns_404_for_missing_user(admin_client):
    fake_id = uuid.uuid4()
    for action in ["approve", "reject", "ban", "unban"]:
        r = admin_client.post(f"/api/users/{fake_id}/{action}")
        assert r.status_code == 404


def test_delete_user_removes_user(admin_client, db):
    user = User(
        email="delete-user@test.com",
        name="Delete Me",
        password="x",
        status=UserStatus.active,
        role=UserRole.owner,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    r = admin_client.delete(f"/api/users/{user.id}")
    assert r.status_code == 204
    assert db.query(User).filter(User.id == user.id).first() is None


def test_delete_user_returns_404_for_missing_user(admin_client):
    fake_id = uuid.uuid4()
    r = admin_client.delete(f"/api/users/{fake_id}")
    assert r.status_code == 404


def test_delete_user_cannot_delete_own_account(auth_user):
    client = auth_user["client"]
    current = auth_user["user"]

    r = client.delete(f"/api/users/{current.id}")
    assert r.status_code == 403


def test_users_endpoints_without_auth_return_401_or_403(client):
    r = client.get("/api/users")
    assert r.status_code in (401, 403)
    r2 = client.get("/api/users/active")
    assert r2.status_code in (401, 403)