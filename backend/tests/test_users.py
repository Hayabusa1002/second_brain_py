import uuid

from app.models.user import User, UserStatus, UserRole


def test_list_all_users_returns_users_array(auth_client, db):
    # Should return all users including the admin/owner created by auth_client
    r = auth_client.get("/api/users")
    assert r.status_code == 200
    data = r.json()
    assert "users" in data
    assert isinstance(data["users"], list)
    assert len(data["users"]) >= 1


def test_list_pending_users_returns_only_pending(auth_client, db):
    # Create a pending user directly in DB
    pending = User(
        email="pending-user@test.com",
        name="Pending User",
        hashed_password="x",
        status=UserStatus.pending,
        role=UserRole.member,
    )
    db.add(pending)
    db.commit()
    db.refresh(pending)

    r = auth_client.get("/api/users/pending")
    assert r.status_code == 200
    data = r.json()
    assert "users" in data
    assert any(u["email"] == "pending-user@test.com" for u in data["users"])


def test_list_active_users_returns_only_active(auth_client, db):
    # Create an active user in DB
    active = User(
        email="active-user@test.com",
        name="Active User",
        hashed_password="x",
        status=UserStatus.active,
        role=UserRole.member,
    )
    db.add(active)
    db.commit()
    db.refresh(active)

    r = auth_client.get("/api/users/active")
    assert r.status_code == 200
    data = r.json()
    assert "users" in data
    assert any(u["email"] == "active-user@test.com" for u in data["users"])


def test_get_user_by_id_returns_200_for_existing_user(auth_client, db):
    # Create a user and fetch it by id
    user = User(
        email="detail-user@test.com",
        name="Detail User",
        hashed_password="x",
        status=UserStatus.active,
        role=UserRole.member,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    r = auth_client.get(f"/api/users/{user.id}")
    assert r.status_code == 200
    data = r.json()
    assert "user" in data
    assert data["user"]["id"] == str(user.id)
    assert data["user"]["email"] == "detail-user@test.com"


def test_get_user_by_id_returns_404_for_missing_user(auth_client):
    # Non-existing user id should return 404
    fake_id = uuid.uuid4()
    r = auth_client.get(f"/api/users/{fake_id}")
    assert r.status_code == 404
    assert r.json()["detail"] == "User not found"


def test_update_user_with_valid_data_returns_200(auth_client, db):
    # Update name and role of an existing user
    user = User(
        email="update-user@test.com",
        name="Old Name",
        hashed_password="x",
        status=UserStatus.active,
        role=UserRole.member,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    r = auth_client.put(
        f"/api/users/{user.id}",
        json={
            "name": "New Name",
            "role": "admin",
        },
    )
    assert r.status_code == 200
    data = r.json()
    assert data["user"]["id"] == str(user.id)
    assert data["user"]["name"] == "New Name"
    assert data["user"]["role"] == "admin"


def test_update_user_returns_404_for_missing_user(auth_client):
    # Updating a non-existing user should return 404
    fake_id = uuid.uuid4()
    r = auth_client.put(
        f"/api/users/{fake_id}",
        json={"name": "Does Not Exist", "role": "member"},
    )
    assert r.status_code == 404
    assert r.json()["detail"] == "User not found"


def test_approve_user_changes_status_to_active(auth_client, db):
    # Approve pending user should set status to active
    user = User(
        email="approve-user@test.com",
        name="Approve User",
        hashed_password="x",
        status=UserStatus.pending,
        role=UserRole.member,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    r = auth_client.post(f"/api/users/{user.id}/approve")
    assert r.status_code == 200
    data = r.json()
    assert data["user"]["status"] == UserStatus.active.value


def test_reject_user_changes_status_to_inactive(auth_client, db):
    # Reject pending user should set status to inactive
    user = User(
        email="reject-user@test.com",
        name="Reject User",
        hashed_password="x",
        status=UserStatus.pending,
        role=UserRole.member,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    r = auth_client.post(f"/api/users/{user.id}/reject")
    assert r.status_code == 200
    data = r.json()
    assert data["user"]["status"] == UserStatus.inactive.value


def test_ban_user_changes_status_to_banned(auth_client, db):
    # Ban user should set status to banned
    user = User(
        email="ban-user@test.com",
        name="Ban User",
        hashed_password="x",
        status=UserStatus.active,
        role=UserRole.member,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    r = auth_client.post(f"/api/users/{user.id}/ban")
    assert r.status_code == 200
    data = r.json()
    assert data["user"]["status"] == UserStatus.banned.value


def test_unban_user_changes_status_to_active(auth_client, db):
    # Unban user should set status back to active
    user = User(
        email="unban-user@test.com",
        name="Unban User",
        hashed_password="x",
        status=UserStatus.banned,
        role=UserRole.member,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    r = auth_client.post(f"/api/users/{user.id}/unban")
    assert r.status_code == 200
    data = r.json()
    assert data["user"]["status"] == UserStatus.active.value


def test_status_change_returns_404_for_missing_user(auth_client):
    # Status change endpoints should return 404 if user does not exist
    fake_id = uuid.uuid4()
    for action in ["approve", "reject", "ban", "unban"]:
        r = auth_client.post(f"/api/users/{fake_id}/{action}")
        assert r.status_code == 404
        assert r.json()["detail"] == "User not found"


def test_delete_user_removes_user(auth_client, db):
    # Deleting another user should return 204
    user = User(
        email="delete-user@test.com",
        name="Delete Me",
        hashed_password="x",
        status=UserStatus.active,
        role=UserRole.member,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    r = auth_client.delete(f"/api/users/{user.id}")
    assert r.status_code == 204

    # User should no longer exist in DB
    assert db.query(User).filter(User.id == user.id).first() is None


def test_delete_user_returns_404_for_missing_user(auth_client):
    # Deleting non-existing user should return 404
    fake_id = uuid.uuid4()
    r = auth_client.delete(f"/api/users/{fake_id}")
    assert r.status_code == 404
    assert r.json()["detail"] == "User not found"


def test_delete_user_cannot_delete_own_account(auth_client, db):
    # Current user should not be able to delete own account
    # auth_client fixture uses email="test@test.com"
    current = db.query(User).filter(User.email == "test@test.com").first()
    assert current is not None

    r = auth_client.delete(f"/api/users/{current.id}")
    assert r.status_code == 400
    assert r.json()["detail"] == "Cannot delete your own account"


def test_users_endpoints_without_auth_return_401_or_403(client):
    # Anonymous user should not be able to access admin users endpoints
    r = client.get("/api/users")
    assert r.status_code in (401, 403)
    r2 = client.get("/api/users/active")
    assert r2.status_code in (401, 403)