from datetime import datetime
from typing import Optional

from fastapi_users import schemas

class UserRead(schemas.BaseUser[int]):
    id: int
    username: str
    email: str
    created_at: datetime 
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False


class UserCreate(schemas.BaseUserCreate):
    email: str
    username: str
    password: str
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False