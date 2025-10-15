import pytest
from datetime import datetime


@pytest.mark.asyncio
async def test_create_product(client, auth_headers, mock_repo):
    mock_repo.get_group.return_value = {
        "id": "group-1",
        "name": "Test Group",
        "ownerId": "test-user-id",
        "members": ["test-user-id"],
        "createdAt": datetime.utcnow(),
        "updatedAt": datetime.utcnow(),
    }

    mock_repo.create_product.return_value = {
        "id": "product-1",
        "groupId": "group-1",
        "name": "Milk",
        "assigneeUserId": None,
        "status": "pending",
        "quantity": 2,
        "notes": "Whole milk",
        "preset": "milk",
        "createdAt": datetime.utcnow(),
        "updatedAt": datetime.utcnow(),
    }

    response = client.post(
        "/api/v1/groups/group-1/products",
        json={
            "name": "Milk",
            "quantity": 2,
            "notes": "Whole milk",
            "preset": "milk"
        },
        headers=auth_headers
    )

    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Milk"
    assert data["quantity"] == 2
    assert data["status"] == "pending"


@pytest.mark.asyncio
async def test_list_products(client, auth_headers, mock_repo):
    mock_repo.get_group.return_value = {
        "id": "group-1",
        "name": "Test Group",
        "ownerId": "test-user-id",
        "members": ["test-user-id"],
        "createdAt": datetime.utcnow(),
        "updatedAt": datetime.utcnow(),
    }

    mock_repo.list_group_products.return_value = [
        {
            "id": "product-1",
            "groupId": "group-1",
            "name": "Milk",
            "assigneeUserId": None,
            "status": "pending",
            "quantity": 2,
            "notes": None,
            "preset": "milk",
            "createdAt": datetime.utcnow(),
            "updatedAt": datetime.utcnow(),
        }
    ]

    response = client.get("/api/v1/groups/group-1/products", headers=auth_headers)

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Milk"


@pytest.mark.asyncio
async def test_update_product_status(client, auth_headers, mock_repo):
    mock_repo.get_group.return_value = {
        "id": "group-1",
        "name": "Test Group",
        "ownerId": "test-user-id",
        "members": ["test-user-id"],
        "createdAt": datetime.utcnow(),
        "updatedAt": datetime.utcnow(),
    }

    mock_repo.get_product.return_value = {
        "id": "product-1",
        "groupId": "group-1",
        "name": "Milk",
        "assigneeUserId": None,
        "status": "pending",
        "quantity": 2,
        "notes": None,
        "preset": "milk",
        "createdAt": datetime.utcnow(),
        "updatedAt": datetime.utcnow(),
    }

    mock_repo.update_product.return_value = {
        "id": "product-1",
        "groupId": "group-1",
        "name": "Milk",
        "assigneeUserId": None,
        "status": "bought",
        "quantity": 2,
        "notes": None,
        "preset": "milk",
        "createdAt": datetime.utcnow(),
        "updatedAt": datetime.utcnow(),
    }

    response = client.patch(
        "/api/v1/groups/group-1/products/product-1",
        json={"status": "bought"},
        headers=auth_headers
    )

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "bought"


@pytest.mark.asyncio
async def test_delete_product(client, auth_headers, mock_repo):
    mock_repo.get_group.return_value = {
        "id": "group-1",
        "name": "Test Group",
        "ownerId": "test-user-id",
        "members": ["test-user-id"],
        "createdAt": datetime.utcnow(),
        "updatedAt": datetime.utcnow(),
    }

    mock_repo.get_product.return_value = {
        "id": "product-1",
        "groupId": "group-1",
        "name": "Milk",
        "assigneeUserId": None,
        "status": "pending",
        "quantity": 2,
        "notes": None,
        "preset": "milk",
        "createdAt": datetime.utcnow(),
        "updatedAt": datetime.utcnow(),
    }

    mock_repo.delete_product.return_value = True

    response = client.delete("/api/v1/groups/group-1/products/product-1", headers=auth_headers)

    assert response.status_code == 204
