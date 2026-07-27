from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime
from typing import Optional, List

# ----- Task Schemas -----
class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None


class Task(TaskBase):
    id: int
    user_id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


# ----- User Schemas -----
class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    tasks: List[Task] = []

    model_config = ConfigDict(from_attributes=True)


# ----- Token Schemas -----
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None
