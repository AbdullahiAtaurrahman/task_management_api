from uuid import uuid4

import pytest

BASE_URL = "/api/v1/auth"


def unique_user():
    suffix = uuid4().hex[:8]

    return {
        "username": f"user_{suffix}",
        "email": f"user_{suffix}@example.com",
        "password": "StrongPass123",
    }


@pytest.mark.asyncio
async def test_register_user(client):
    user_data = unique_user()

    response = await client.post(
        f"{BASE_URL}/register",
        json=user_data,
    )

    assert response.status_code == 201

    data = response.json()

    assert data["id"] is not None
    assert data["username"] == user_data["username"]
    assert data["email"] == user_data["email"]
    assert "password" not in data
    assert "hashed_password" not in data


@pytest.mark.asyncio
async def test_register_duplicate_username(client):
    user_data = unique_user()

    first_response = await client.post(
        f"{BASE_URL}/register",
        json=user_data,
    )

    assert first_response.status_code == 201

    duplicate_user = {
        **unique_user(),
        "username": user_data["username"],
    }

    response = await client.post(
        f"{BASE_URL}/register",
        json=duplicate_user,
    )

    assert response.status_code == 409


@pytest.mark.asyncio
async def test_register_duplicate_email(client):
    user_data = unique_user()

    first_response = await client.post(
        f"{BASE_URL}/register",
        json=user_data,
    )

    assert first_response.status_code == 201

    duplicate_user = {
        **unique_user(),
        "email": user_data["email"],
    }

    response = await client.post(
        f"{BASE_URL}/register",
        json=duplicate_user,
    )

    assert response.status_code == 409


@pytest.mark.asyncio
async def test_register_invalid_email(client):
    user_data = unique_user()
    user_data["email"] = "not-an-email"

    response = await client.post(
        f"{BASE_URL}/register",
        json=user_data,
    )

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_register_short_password(client):
    user_data = unique_user()
    user_data["password"] = "short"

    response = await client.post(
        f"{BASE_URL}/register",
        json=user_data,
    )

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_register_short_username(client):
    user_data = unique_user()
    user_data["username"] = "ab"

    response = await client.post(
        f"{BASE_URL}/register",
        json=user_data,
    )

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_login_success(client):
    user_data = unique_user()

    register_response = await client.post(
        f"{BASE_URL}/register",
        json=user_data,
    )

    assert register_response.status_code == 201

    response = await client.post(
        f"{BASE_URL}/login",
        data={
            "username": user_data["email"],
            "password": user_data["password"],
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["access_token"]
    assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_login_wrong_password(client):
    user_data = unique_user()

    register_response = await client.post(
        f"{BASE_URL}/register",
        json=user_data,
    )

    assert register_response.status_code == 201

    response = await client.post(
        f"{BASE_URL}/login",
        data={
            "username": user_data["email"],
            "password": "WrongPassword123",
        },
    )

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_login_unknown_user(client):
    user_data = unique_user()

    response = await client.post(
        f"{BASE_URL}/login",
        data={
            "username": user_data["email"],
            "password": user_data["password"],
        },
    )

    assert response.status_code == 401
