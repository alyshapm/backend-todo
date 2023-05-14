from typing import Union, Optional
from pydantic import BaseModel

# TODOS
class TodoBase(BaseModel):
    title: str
    description: Union[str, None] = None

class TodoCreate(TodoBase):
    pass

class Todo(TodoBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True

class TodoUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None

# USER
class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    todos: list[Todo] = []

    class Config:
        orm_mode = True

class UserUpdate(BaseModel):
    email: Optional[str] = None