from datetime import datetime
import uuid
from app.core.db import users_collection
from app.core.security import get_password_hash
from app.models.user import UserCreate, UserUpdate, User, UserInDB
from app.api.dependencies import get_user_by_email

async def create_user(user: UserCreate) -> User:
    # Check if user with email already exists
    if await get_user_by_email(user.user_email):
        return None
    
    now = datetime.utcnow()
    user_id = str(uuid.uuid4())
    
    user_in_db = UserInDB(
        user_id=user_id,
        user_name=user.user_name,
        user_email=user.user_email,
        hashed_password=get_password_hash(user.password),
        created_on=now,
        last_update=now
    )
    
    await users_collection.insert_one(user_in_db.dict())
    
    return User(
        user_id=user_id,
        user_name=user.user_name,
        user_email=user.user_email,
        created_on=now,
        last_update=now
    )

async def update_user(user_id: str, user_update: UserUpdate) -> User:
    now = datetime.utcnow()
    
    update_data = {
        "user_name": user_update.user_name,
        "user_email": user_update.user_email,
        "last_update": now
    }
    
    await users_collection.update_one(
        {"user_id": user_id},
        {"$set": update_data}
    )
    
    updated_user = await users_collection.find_one({"user_id": user_id})
    return User(**updated_user)