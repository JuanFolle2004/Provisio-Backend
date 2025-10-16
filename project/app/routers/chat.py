from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from app.models import ChatMessageResponse
from app.deps import get_user_id
from app.repositories.firestore import repo


router = APIRouter(prefix="/groups/{group_id}/messages", tags=["chat"])


@router.get("", response_model=List[ChatMessageResponse])
async def get_messages(
    group_id: str,
    limit: int = 100,
    user_id: str = Depends(get_user_id)
):
    group = await repo.get_group(group_id)
    if not group:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Group not found")

    if user_id not in group.get("members", []):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not a member of this group")

    messages = await repo.list_group_messages(group_id, limit)
    return messages
