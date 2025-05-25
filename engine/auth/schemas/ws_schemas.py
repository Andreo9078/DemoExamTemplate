from pydantic import BaseModel


class AuthDataSchema(BaseModel):
    token: str

    class Config:
        from_attributes = True
