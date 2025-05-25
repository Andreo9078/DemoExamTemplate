import secrets
import string
from abc import ABC, abstractmethod
from typing import Optional, Union

from pwdlib import PasswordHash
from pwdlib.hashers.argon2 import Argon2Hasher


class BasePasswordHelper(ABC):
    @abstractmethod
    def verify_and_update(self, plain_password: str, hashed_password: str): ...

    @abstractmethod
    def hash(self, password: str) -> str: ...

    @abstractmethod
    def generate(self) -> str: ...


class PasswordHelper(BasePasswordHelper):
    def __init__(self, password_hash: Optional[PasswordHash] = None) -> None:
        if password_hash is None:
            self.password_hash = PasswordHash((Argon2Hasher(),))
        else:
            self.password_hash = password_hash  # pragma: no cover

    def verify_and_update(
        self, plain_password: str, hashed_password: str
    ) -> tuple[bool, Union[str, None]]:
        return self.password_hash.verify_and_update(plain_password, hashed_password)

    def hash(self, password: str) -> str:
        return self.password_hash.hash(password)

    def generate(self) -> str:
        return secrets.token_urlsafe()


from datetime import datetime, timezone, timedelta
from typing import Optional, Any

import jwt


def generate_jwt(
    data: dict,
    secret: str,
    algorithm: str,
    lifetime_seconds: Optional[int] = None,
) -> str:
    payload = data.copy()
    if lifetime_seconds:
        expire = datetime.now(timezone.utc) + timedelta(seconds=int(lifetime_seconds))
        payload["exp"] = expire
    return jwt.encode(payload, secret, algorithm=algorithm)


def decode_jwt(
    encoded_jwt: str,
    secret: str,
    audience: list[str],
    algorithms: list[str],
) -> dict[str, Any]:
    return jwt.decode(
        encoded_jwt,
        secret,
        audience=audience,
        algorithms=algorithms,
    )


from typing import Callable

from fastapi.encoders import jsonable_encoder
from starlette.requests import Request
from starlette.responses import JSONResponse


def create_handler(code: int) -> Callable:
    async def json_resp_handler(request: Request, exc: Exception) -> JSONResponse:
        return JSONResponse(
            status_code=code,
            content=jsonable_encoder(
                {
                    "detail": [
                        {
                            "loc": ["body"],
                            "msg": str(exc),
                            "type": exc.__class__.__name__,
                        }
                    ]
                }
            ),
        )

    return json_resp_handler


from abc import ABC
from copy import copy
from typing import Any


class RegistryException(Exception):
    def __init__(self, entity_id: Any) -> None:
        self.entity_id = entity_id


class EntityDoesNotExist(RegistryException):
    def __str__(self) -> str:
        return f"Entity with id '{self.entity_id}' does not exist."


class EntityAlreadyExists(RegistryException):
    def __str__(self) -> str:
        return f"Entity with id '{self.entity_id}' already exists."


class BaseRegistry[ID, EntityType](ABC):
    def __init__(self) -> None:
        self._entities: dict[ID, EntityType] = {}

    @property
    def entities(self) -> dict[ID, EntityType]:
        return copy(self._entities)

    def register(self, id_: ID, value: EntityType) -> None:
        if id_ in self._entities:
            raise EntityAlreadyExists(id_)

        self._entities[id_] = value

    def get_entity(self, id_: ID) -> EntityType:
        entity = self._entities.get(id_)
        if entity is None:
            raise EntityDoesNotExist(id_)

        return entity

    def include_register(self, register: "BaseRegistry[ID, EntityType]") -> None:
        for id_, entity in register.entities.items():
            self.register(id_, entity)


from typing import Type, Callable


class ExceptionRegistry(BaseRegistry[Type[Exception], Callable]):
    @property
    def exceptions(self):
        return self.entities

    def exception(self, handler: Callable):
        def decorator(exception: Type[Exception]):
            self.register(exception, handler)
            return exception

        return decorator

    def handle_exceptions(
        self, handler: Callable[[Type[Exception], Callable], None]
    ) -> None:
        for exception, func in self._entities.items():
            handler(exception, func)

    def __call__(self, handler: Callable[[Type[Exception], Callable], None]) -> None:
        self.handle_exceptions(handler)


def generate_alphanum_crypt_string(length):
    letters_and_digits = string.ascii_letters + string.digits
    crypt_rand_string = "".join(
        secrets.choice(letters_and_digits) for i in range(length)
    )

    return crypt_rand_string
