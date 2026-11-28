from datetime import datetime, timedelta, timezone
from uuid import uuid4

import pytest

TASKS_URL = "/api/v1/tasks"
AUTH_URL = "/api/v1/auth"


def unique_user():
    suffix = uuid4().hex[:8]

    return {
        "username": f"user_{suffix}",
        "email": f"user_{suffix}@example.com",
        "password": "StrongPass123",
    }


async def create_user_and_get_token(client):
    user_data = unique_user()

    register_response = await client.post(
        f"{AUTH_URL}/register",
        json=user_data,
    )

    assert register_response.status_code == 201

    login_response = await client.post(
        f"{AUTH_URL}/login",
        data={
            "username": user_data["username"],
            "password": user_data["password"],
        },
    )

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    return {"Authorization": f"Bearer {token}"}


def valid_task_data():
    return {
        "title": "Complete project",
        "description": "Finish the API project",
        "priority": "medium",
        "completed": False,
        "due_date": (datetime.now(timezone.utc) + timedelta(days=7)).isoformat(),
    }


@pytest.mark.asyncio
async def test_get_tasks(client):
    headers = await create_user_and_get_token(client)

    response = await client.get(
        TASKS_URL,
        headers=headers,
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert response.json() == []


@pytest.mark.asyncio
async def test_create_task(client):
    headers = await create_user_and_get_token(client)
    task_data = valid_task_data()

    response = await client.post(
        TASKS_URL,
        json=task_data,
        headers=headers,
    )

    assert response.status_code == 201

    data = response.json()

    assert data["id"] is not None
    assert data["title"] == task_data["title"]
    assert data["description"] == task_data["description"]
    assert data["priority"] == task_data["priority"]
    assert data["completed"] is False
    assert data["user_id"] is not None


@pytest.mark.asyncio
async def test_get_task_by_id(client):
    headers = await create_user_and_get_token(client)

    create_response = await client.post(
        TASKS_URL,
        json=valid_task_data(),
        headers=headers,
    )

    assert create_response.status_code == 201

    task_id = create_response.json()["id"]

    response = await client.get(
        f"{TASKS_URL}/{task_id}",
        headers=headers,
    )

    assert response.status_code == 200
    assert response.json()["id"] == task_id


@pytest.mark.asyncio
async def test_update_task(client):
    headers = await create_user_and_get_token(client)

    create_response = await client.post(
        TASKS_URL,
        json=valid_task_data(),
        headers=headers,
    )

    assert create_response.status_code == 201

    task_id = create_response.json()["id"]

    response = await client.patch(
        f"{TASKS_URL}/{task_id}",
        json={
            "title": "Updated task title",
            "completed": True,
        },
        headers=headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["title"] == "Updated task title"
    assert data["completed"] is True


@pytest.mark.asyncio
async def test_delete_task(client):
    headers = await create_user_and_get_token(client)

    create_response = await client.post(
        TASKS_URL,
        json=valid_task_data(),
        headers=headers,
    )

    assert create_response.status_code == 201

    task_id = create_response.json()["id"]

    response = await client.delete(
        f"{TASKS_URL}/{task_id}",
        headers=headers,
    )

    assert response.status_code == 204


@pytest.mark.asyncio
async def test_get_nonexistent_task(client):
    headers = await create_user_and_get_token(client)

    response = await client.get(
        f"{TASKS_URL}/999999",
        headers=headers,
    )

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_update_nonexistent_task(client):
    headers = await create_user_and_get_token(client)

    response = await client.patch(
        f"{TASKS_URL}/999999",
        json={"title": "Updated title"},
        headers=headers,
    )

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_delete_nonexistent_task(client):
    headers = await create_user_and_get_token(client)

    response = await client.delete(
        f"{TASKS_URL}/999999",
        headers=headers,
    )

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_create_task_without_authentication(client):
    response = await client.post(
        TASKS_URL,
        json=valid_task_data(),
    )

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_get_tasks_without_authentication(client):
    response = await client.get(TASKS_URL)

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_create_task_with_invalid_priority(client):
    headers = await create_user_and_get_token(client)
    task_data = valid_task_data()
    task_data["priority"] = "urgent"

    response = await client.post(
        TASKS_URL,
        json=task_data,
        headers=headers,
    )

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_create_task_with_blank_title(client):
    headers = await create_user_and_get_token(client)
    task_data = valid_task_data()
    task_data["title"] = "   "

    response = await client.post(
        TASKS_URL,
        json=task_data,
        headers=headers,
    )

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_update_task_with_null_title(client):
    headers = await create_user_and_get_token(client)

    create_response = await client.post(
        TASKS_URL,
        json=valid_task_data(),
        headers=headers,
    )

    assert create_response.status_code == 201

    task_id = create_response.json()["id"]

    response = await client.patch(
        f"{TASKS_URL}/{task_id}",
        json={"title": None},
        headers=headers,
    )

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_user_cannot_access_another_users_task(client):
    user_a_headers = await create_user_and_get_token(client)
    user_b_headers = await create_user_and_get_token(client)

    create_response = await client.post(
        TASKS_URL,
        json=valid_task_data(),
        headers=user_a_headers,
    )

    assert create_response.status_code == 201

    task_id = create_response.json()["id"]

    response = await client.get(
        f"{TASKS_URL}/{task_id}",
        headers=user_b_headers,
    )

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_user_cannot_update_another_users_task(client):
    user_a_headers = await create_user_and_get_token(client)
    user_b_headers = await create_user_and_get_token(client)

    create_response = await client.post(
        TASKS_URL,
        json=valid_task_data(),
        headers=user_a_headers,
    )

    assert create_response.status_code == 201

    task_id = create_response.json()["id"]

    response = await client.patch(
        f"{TASKS_URL}/{task_id}",
        json={"title": "Unauthorized update"},
        headers=user_b_headers,
    )

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_user_cannot_delete_another_users_task(client):
    user_a_headers = await create_user_and_get_token(client)
    user_b_headers = await create_user_and_get_token(client)

    create_response = await client.post(
        TASKS_URL,
        json=valid_task_data(),
        headers=user_a_headers,
    )

    assert create_response.status_code == 201

    task_id = create_response.json()["id"]

    response = await client.delete(
        f"{TASKS_URL}/{task_id}",
        headers=user_b_headers,
    )

    assert response.status_code == 404
