from fastapi.security import OAuth2PasswordRequestForm

from .. import exceptions
from ..domain import User
from ..exceptions import UserNotExists, RoleDoesNotExist
from ..repos.roles_repo import RoleRepository
from ..repos.user_repo import UserRepository
from ..schemas.schemes import (
    UserCreate,
    UserGenerate,
    UserUnHashedPass,
    UserUpdate,
)
from engine.utils import generate_alphanum_crypt_string
from engine.utils import BasePasswordHelper


class UserManager:
    def __init__(
        self,
        user_repo: UserRepository,
        role_repo: RoleRepository,
        password_helper: BasePasswordHelper,
    ):
        self.user_repo = user_repo
        self.role_repo = role_repo
        self.password_helper = password_helper

    async def get(self, user_id: int) -> User:
        user = await self.user_repo.get(user_id)
        if user is None:
            raise UserNotExists

        return user

    async def get_all(self) -> list[User]:
        users = await self.user_repo.get_all()
        return users

    async def get_by_username(self, username: str):
        user = await self.user_repo.get_by_username(username)

        if not user:
            raise UserNotExists

        return user

    async def create(self, user: UserCreate) -> User:
        role = await self.role_repo.get(user.role_id)
        if role is None:
            raise RoleDoesNotExist(user.role_id)

        existing_user = await self.user_repo.get_by_username(user.username)

        if existing_user is not None:
            raise exceptions.UserAlreadyExists

        user_dict = user.model_dump()
        password = user_dict.pop("password")
        user_dict["hashed_password"] = self.password_helper.hash(password)

        created_user = await self.user_repo.create(user_dict)

        return created_user

    async def update(self, user_id: int, user: UserUpdate) -> User:
        existing_user = await self.user_repo.get(user_id)
        if existing_user is None:
            raise UserNotExists

        updated_user = await self.user_repo.update(
            user_id, user.model_dump(exclude_none=True)
        )

        return updated_user

    async def delete(self, username: int) -> None:
        existing_user = await self.user_repo.get(username)
        if existing_user is None:
            raise UserNotExists

        await self.user_repo.delete(existing_user.id)

    async def reset_password(self, username: str) -> UserUnHashedPass:
        user = await self.get_by_username(username)
        new_pass = generate_alphanum_crypt_string(16)
        user_update = UserUpdate(username=username, password=new_pass)
        await self.update(user.id, user_update)
        return UserUnHashedPass(
            user_id=user.id,
            username=user.username,
            password=new_pass,
            role=user.role.name,
        )

    async def generate_user(self, generate_scheme: UserGenerate) -> UserUnHashedPass:
        username = generate_alphanum_crypt_string(16)
        password = generate_alphanum_crypt_string(16)

        user_create = UserCreate(
            username=username, password=password, role_id=generate_scheme.role_id
        )
        created_user = await self.create(user_create)

        role = created_user.role
        generated_user = UserUnHashedPass(
            user_id=created_user.id,
            username=username,
            password=password,
            role=role.name,
        )

        return generated_user

    async def authenticate(self, credentials: OAuth2PasswordRequestForm):
        try:
            user = await self.get_by_username(credentials.username)
        except exceptions.UserNotExists:
            # Run the hasher to mitigate timing attack
            # Inspired from Django: https://code.djangoproject.com/ticket/20760
            self.password_helper.hash(credentials.password)
            return None

        verified, updated_password_hash = self.password_helper.verify_and_update(
            credentials.password, user.hashed_password
        )
        if not verified:
            return None
        # Update password hash to a more robust one if needed
        if updated_password_hash is not None:
            await self.user_repo.update(
                user.id, {"hashed_password": updated_password_hash}
            )

        return user
