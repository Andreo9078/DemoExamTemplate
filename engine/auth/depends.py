from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from engine.config import SECRET, JWT_LIFETIME
from engine.utils import PasswordHelper
from .domain import User
from .repos.roles_repo import RoleRepository, get_role_repository
from .repos.user_repo import UserRepository, get_user_repository
from .services.auth_service import AuthService
from .services.role_service import RoleService
from .services.user_manager import UserManager


def get_user_manager(
    user_repo: Annotated[UserRepository, Depends(get_user_repository)],
    role_repo: Annotated[RoleRepository, Depends(get_role_repository)],
) -> UserManager:
    return UserManager(user_repo, role_repo, PasswordHelper())


def get_auth_service() -> AuthService:
    return AuthService(SECRET, JWT_LIFETIME)


# Можно заюзать фабричный метод,
# чтобы добавить проверки:
# активен пользователь,
# является ли он суперпользователем и тд
async def get_current_user(
    token: Annotated[str, Depends(OAuth2PasswordBearer(tokenUrl="login"))],
    user_manager: Annotated[UserManager, Depends(get_user_manager)],
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
) -> User:
    user = await auth_service.read_token(token, user_manager)
    if user is None:
        raise HTTPException(status_code=401, detail="Unauthorized")

    return user


def get_role_service(
    role_repo: Annotated[RoleRepository, Depends(get_role_repository)],
    curr_user: Annotated[User, Depends(get_current_user)],
) -> RoleService:
    return RoleService(role_repo, curr_user)
