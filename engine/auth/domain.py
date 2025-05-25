from pydantic import BaseModel


class User(BaseModel):
    id: int
    username: str
    hashed_password: str
    is_active: bool = True
    is_superuser: bool = True
    is_verified: bool = True

    role: "Role"

    class Config:
        from_attributes = True


class Role(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class CameraOwner(BaseModel):
    id: int
    owner_id: int
    camera_id: int

    class Config:
        from_attributes = True
