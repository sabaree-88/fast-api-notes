from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from app.core.config import settings
from app.core.db import users_collection
from app.models.user import UserInDB, TokenData
from typing import Optional, Union

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/token")

async def get_user(user_id: str) -> Optional[UserInDB]:
    """Fetch a user by their user_id from MongoDB."""
    user = await users_collection.find_one({"user_id": user_id})
    return UserInDB(**user) if user else None

async def get_user_by_email(email: str) -> Optional[UserInDB]:
    """Fetch a user by their email from MongoDB."""
    user = await users_collection.find_one({"user_email": email})
    return UserInDB(**user) if user else None

async def get_current_user(token: str = Depends(oauth2_scheme)) -> UserInDB:
    """Extract and validate the current user from the JWT token."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: Optional[str] = payload.get("sub")
        
        if not user_id:
            raise credentials_exception
        
        token_data = TokenData(user_id=user_id)

    except JWTError:
        raise credentials_exception
    
    # Fetch user from database
    user = await get_user(token_data.user_id)
    
    if not user:
        raise credentials_exception

    return user
