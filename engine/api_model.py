from typing import Optional

from pydantic import BaseModel


class PathModel(BaseModel):
    path: str
    message: Optional[str] = None


class HelloModel(BaseModel):
    name: str
    message: Optional[str]
