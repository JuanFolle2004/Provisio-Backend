from fastapi import APIRouter, Depends, HTTPException, status
from app.models import UserResponse
from app.deps import get_current_user
from app.repositories.firestore import repo


router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: dict = Depends(get_current_user)):
    user_id = current_user.get("uid")
    user = await repo.get_user(user_id)

    if not user:
        user_data = {
            "id": user_id,
            "username": current_user.get("name", current_user.get("email", "").split("@")[0]),
            "displayName": current_user.get("name", "User"),
            "email": current_user.get("email", ""),
            "photoURL": current_user.get("picture"),
        }
        user = await repo.create_user(user_id, user_data)

    return user
