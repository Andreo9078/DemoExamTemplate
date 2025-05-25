from abc import ABC, abstractmethod
from typing import Optional, Any

from fastapi import Response
from fastapi.responses import JSONResponse
from jwt.exceptions import PyJWTError
from pydantic import BaseModel

from engine.utils import generate_jwt, decode_jwt
from .. import exceptions
from ..domain import User
from ..services.user_manager import UserManager


class BearerResponse(BaseModel):
    access_token: str
    token_type: str


class BaseIdParser[ID](ABC):
    @abstractmethod
    def parse(self, id_: Any) -> ID: ...


class IntParser(BaseIdParser[int]):
    def parse(self, id_: Any) -> int:
        return int(id_)


class AuthService:
    def __init__(
        self,
        secret: str,
        lifetime_seconds: Optional[int],
        token_audience: Optional[list[str]] = None,
        algorithm: str = "HS256",
        public_key: Optional[str] = None,
        id_parser: Optional[BaseIdParser] = None,
    ) -> None:
        self._secret = secret
        self._lifetime_seconds = lifetime_seconds
        self._token_audience = token_audience or ["cam:auth"]
        self._algorithm = algorithm
        self._public_key = public_key
        self._id_parser = id_parser or IntParser()

    @property
    def encode_key(self) -> str:
        return self._secret

    @property
    def decode_key(self) -> str:
        return self._public_key or self._secret

    async def login(self, user: User) -> Response:
        token = await self.write_token(user)
        response_model = BearerResponse(access_token=token, token_type="bearer")
        return JSONResponse(response_model.model_dump())

    async def write_token(self, user: User) -> str:
        data = {"sub": str(user.id), "aud": self._token_audience}
        return generate_jwt(
            data,
            self.encode_key,
            lifetime_seconds=self._lifetime_seconds,
            algorithm=self._algorithm,
        )

    async def read_token(
        self, token: Optional[str], user_manager: UserManager
    ) -> Optional[User]:
        if token is None:
            return None

        try:
            data = decode_jwt(
                token,
                self.decode_key,
                self._token_audience,
                algorithms=[self._algorithm],
            )
            user_id = self._id_parser.parse(data.get("sub"))
            if user_id is None:
                return None
        except PyJWTError:
            return None

        try:
            return await user_manager.get(user_id)
        except exceptions.UserNotExists:
            return None
