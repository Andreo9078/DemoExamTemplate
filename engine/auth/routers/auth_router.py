from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from engine.exceptions import PermissionDenied
from ..depends import get_user_manager, get_auth_service, get_current_user
from ..domain import User
from ..schemas.schemes import UserGenerate, UserUnHashedPass
from ..services.auth_service import AuthService
from ..services.user_manager import UserManager

router = APIRouter()


@router.post("/login")
async def login(
    credentials: OAuth2PasswordRequestForm = Depends(),
    user_manager: UserManager = Depends(get_user_manager),
    auth_service: AuthService = Depends(get_auth_service),
):
    user = await user_manager.authenticate(credentials)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="LOGIN_BAD_CREDENTIALS",
        )
    response = await auth_service.login(user)

    return response


@router.post("/generate_user")
async def generate_user(
    user_generate: UserGenerate,
    curr_user: Annotated[User, Depends(get_current_user)],
    user_manager: UserManager = Depends(get_user_manager),
) -> UserUnHashedPass:
    if curr_user.role.name != "admin":
        raise PermissionDenied

    return await user_manager.generate_user(user_generate)


@router.get("/users")
async def get_users(
    curr_user: Annotated[User, Depends(get_current_user)],
    user_manager: UserManager = Depends(get_user_manager),
):
    if curr_user.role.name != "admin":
        raise PermissionDenied

    users = await user_manager.get_all()

    return users
