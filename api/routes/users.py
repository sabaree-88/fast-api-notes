from fastapi import APIRouter, HTTPException, Depends, status
from models.user import UserCreate, User, UserUpdate, UserInDB
from services import user_service
from api.dependencies import get_current_user

router = APIRouter(tags=["users"])

@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate):
    """Create a new user. Returns a 400 error if the email is already registered."""
    existing_user = await user_service.get_user_by_email(user.user_email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    return await user_service.create_user(user)

@router.get("/me", response_model=User)
async def read_users_me(current_user: UserInDB = Depends(get_current_user)):
    """Retrieve the currently authenticated user's details."""
    return current_user

@router.put("/me", response_model=User)
async def update_user_me(
    user_update: UserUpdate,
    current_user: UserInDB = Depends(get_current_user)
):
    """Update the authenticated user's profile."""
    updated_user = await user_service.update_user(current_user.user_id, user_update)
    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to update user"
        )
    return updated_user
