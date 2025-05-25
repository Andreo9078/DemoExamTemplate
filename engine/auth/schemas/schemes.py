from typing import Optional

from pydantic import BaseModel


class UserRead(BaseModel):
    username: str
    role_id: int


class UserCreate(BaseModel):
    username: str
    password: str
    role_id: int

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    role_id: Optional[int] = None
    username: Optional[str] = None
    password: Optional[str] = None

    class Config:
        from_attributes = True


class UserGenerate(BaseModel):
    role_id: int


class UserUnHashedPass(BaseModel):
    user_id: int
    username: str
    password: str
    role: str


class UserFilters(BaseModel):
    role_id: Optional[int] = None
    offset: Optional[int] = None
    limit: Optional[int] = None


class CreateRole(BaseModel):
    name: str


class UpdateRole(BaseModel):
    name: str
