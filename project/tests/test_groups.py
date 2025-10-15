import pytest
from datetime import datetime
from unittest.mock import AsyncMock


@pytest.mark.asyncio
async def test_create_group(client, auth_headers, mock_repo):
    mock_repo.create_group.return_value = {
        "id": "group-1",
        "name": "Test Group",
        "description": "A test group",
        "ownerId": "test-user-id",
        "members": ["test-user-id"],
        "createdAt": datetime.utcnow(),
        "updatedAt": datetime.utcnow(),
    }

    response = client.post(
        "/api/v1/groups",
        json={"name": "Test Group", "description": "A test group"},
        headers=auth_headers
    )

    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Group"
    assert data["ownerId"] == "test-user-id"
    assert "test-user-id" in data["members"]


@pytest.mark.asyncio
async def test_list_groups(client, auth_headers, mock_repo):
    mock_repo.list_user_groups.return_value = [
        {
            "id": "group-1",
            "name": "Test Group 1",
            "description": None,
            "ownerId": "test-user-id",
            "members": ["test-user-id"],
            "createdAt": datetime.utcnow(),
            "updatedAt": datetime.utcnow(),
        }
    ]

    response = client.get("/api/v1/groups", headers=auth_headers)

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Test Group 1"


@pytest.mark.asyncio
async def test_get_group(client, auth_headers, mock_repo):
    mock_repo.get_group.return_value = {
        "id": "group-1",
        "name": "Test Group",
        "description": None,
        "ownerId": "test-user-id",
        "members": ["test-user-id"],
        "createdAt": datetime.utcnow(),
        "updatedAt": datetime.utcnow(),
    }

    response = client.get("/api/v1/groups/group-1", headers=auth_headers)

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == "group-1"
    assert data["name"] == "Test Group"


@pytest.mark.asyncio
async def test_add_member(client, auth_headers, mock_repo):
    mock_repo.get_group.return_value = {
        "id": "group-1",
        "name": "Test Group",
        "description": None,
        "ownerId": "test-user-id",
        "members": ["test-user-id"],
        "createdAt": datetime.utcnow(),
        "updatedAt": datetime.utcnow(),
    }

    mock_repo.add_member_to_group.return_value = {
        "id": "group-1",
        "name": "Test Group",
        "description": None,
        "ownerId": "test-user-id",
        "members": ["test-user-id", "member-2"],
        "createdAt": datetime.utcnow(),
        "updatedAt": datetime.utcnow(),
    }

    response = client.post(
        "/api/v1/groups/group-1/members/member-2",
        headers=auth_headers
    )

    assert response.status_code == 200
    data = response.json()
    assert "member-2" in data["members"]


@pytest.mark.asyncio
async def test_delete_group(client, auth_headers, mock_repo):
    mock_repo.get_group.return_value = {
        "id": "group-1",
        "name": "Test Group",
        "description": None,
        "ownerId": "test-user-id",
        "members": ["test-user-id"],
        "createdAt": datetime.utcnow(),
        "updatedAt": datetime.utcnow(),
    }

    mock_repo.delete_group.return_value = True

    response = client.delete("/api/v1/groups/group-1", headers=auth_headers)

    assert response.status_code == 204
