from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, ConfigDict

class UserBase(BaseModel):
    user_name: str
    user_email: EmailStr

class UserCreate(UserBase):
    password: str

class UserUpdate(UserBase):
    pass

class UserInDB(UserBase):
    user_id: str
    hashed_password: str
    created_on: datetime
    last_update: datetime

    model_config = ConfigDict(
        from_attributes=True,  # ✅ Replaces 'orm_mode'
        json_schema_extra={    # ✅ Replaces 'schema_extra'
            "example": {
                "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                "user_name": "John Doe",
                "user_email": "john@example.com",
                "hashed_password": "hashedpassword",
                "created_on": "2023-01-01T00:00:00",
                "last_update": "2023-01-01T00:00:00"
            }
        }
    )

class User(UserBase):
    user_id: str
    created_on: datetime
    last_update: datetime

    model_config = ConfigDict(
        from_attributes=True,  # ✅ Fix for 'orm_mode'
        json_schema_extra={    # ✅ Fix for 'schema_extra'
            "example": {
                "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                "user_name": "John Doe",
                "user_email": "john@example.com",
                "created_on": "2023-01-01T00:00:00",
                "last_update": "2023-01-01T00:00:00"
            }
        }
    )

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user_id: Optional[str] = None
