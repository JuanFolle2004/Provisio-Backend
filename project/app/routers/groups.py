from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from app.models import GroupCreate, GroupResponse
from app.deps import get_user_id
from app.repositories.firestore import repo


router = APIRouter(prefix="/groups", tags=["groups"])


@router.post("", response_model=GroupResponse, status_code=status.HTTP_201_CREATED)
async def create_group(group: GroupCreate, user_id: str = Depends(get_user_id)):
    group_data = {
        "name": group.name,
        "description": group.description,
        "ownerId": user_id,
        "members": [user_id],
    }
    new_group = await repo.create_group(group_data)
    return new_group


@router.get("", response_model=List[GroupResponse])
async def list_groups(user_id: str = Depends(get_user_id)):
    groups = await repo.list_user_groups(user_id)
    return groups


@router.get("/{group_id}", response_model=GroupResponse)
async def get_group(group_id: str, user_id: str = Depends(get_user_id)):
    group = await repo.get_group(group_id)
    if not group:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Group not found")

    if user_id not in group.get("members", []):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not a member of this group")

    return group


@router.delete("/{group_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_group(group_id: str, user_id: str = Depends(get_user_id)):
    group = await repo.get_group(group_id)
    if not group:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Group not found")

    if group.get("ownerId") != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only owner can delete group")

    await repo.delete_group(group_id)


@router.post("/{group_id}/members/{member_id}", response_model=GroupResponse)
async def add_member(group_id: str, member_id: str, user_id: str = Depends(get_user_id)):
    group = await repo.get_group(group_id)
    if not group:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Group not found")

    if group.get("ownerId") != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only owner can add members")

    updated_group = await repo.add_member_to_group(group_id, member_id)
    return updated_group


@router.delete("/{group_id}/members/{member_id}", response_model=GroupResponse)
async def remove_member(group_id: str, member_id: str, user_id: str = Depends(get_user_id)):
    group = await repo.get_group(group_id)
    if not group:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Group not found")

    if group.get("ownerId") != user_id and member_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only owner can remove members")

    updated_group = await repo.remove_member_from_group(group_id, member_id)
    return updated_group
