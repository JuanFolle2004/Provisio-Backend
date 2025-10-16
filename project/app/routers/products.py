from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from project.app.models import ProductCreate, ProductUpdate, ProductResponse
from project.app.deps import get_user_id
from project.app.repositories.firestore import repo


router = APIRouter(prefix="/groups/{group_id}/products", tags=["products"])


@router.post("", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(
    group_id: str,
    product: ProductCreate,
    user_id: str = Depends(get_user_id)
):
    group = await repo.get_group(group_id)
    if not group:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Group not found")

    if user_id not in group.get("members", []):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not a member of this group")

    product_data = {
        "groupId": group_id,
        "name": product.name,
        "assigneeUserId": product.assigneeUserId,
        "status": product.status,
        "quantity": product.quantity,
        "notes": product.notes,
        "preset": product.preset,
    }
    new_product = await repo.create_product(product_data)
    return new_product


@router.get("", response_model=List[ProductResponse])
async def list_products(group_id: str, user_id: str = Depends(get_user_id)):
    group = await repo.get_group(group_id)
    if not group:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Group not found")

    if user_id not in group.get("members", []):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not a member of this group")

    products = await repo.list_group_products(group_id)
    return products


@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(
    group_id: str,
    product_id: str,
    user_id: str = Depends(get_user_id)
):
    group = await repo.get_group(group_id)
    if not group:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Group not found")

    if user_id not in group.get("members", []):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not a member of this group")

    product = await repo.get_product(product_id)
    if not product or product.get("groupId") != group_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

    return product


@router.patch("/{product_id}", response_model=ProductResponse)
async def update_product(
    group_id: str,
    product_id: str,
    product_update: ProductUpdate,
    user_id: str = Depends(get_user_id)
):
    group = await repo.get_group(group_id)
    if not group:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Group not found")

    if user_id not in group.get("members", []):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not a member of this group")

    product = await repo.get_product(product_id)
    if not product or product.get("groupId") != group_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

    update_data = product_update.model_dump(exclude_unset=True)
    updated_product = await repo.update_product(product_id, update_data)
    return updated_product


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    group_id: str,
    product_id: str,
    user_id: str = Depends(get_user_id)
):
    group = await repo.get_group(group_id)
    if not group:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Group not found")

    if user_id not in group.get("members", []):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not a member of this group")

    product = await repo.get_product(product_id)
    if not product or product.get("groupId") != group_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

    await repo.delete_product(product_id)
