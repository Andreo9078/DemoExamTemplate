from typing import Annotated

from fastapi import APIRouter, Depends

from ..depends import get_role_service
from ..domain import Role
from ..schemas.schemes import CreateRole, UpdateRole
from ..services.role_service import RoleService

router = APIRouter(prefix="/roles")


@router.post("", response_model=Role)
async def create_role(
    roles_service: Annotated[RoleService, Depends(get_role_service)], role: CreateRole
):
    created_role = await roles_service.create(role)
    return created_role


@router.get("", response_model=list[Role])
async def get_roles(roles_service: Annotated[RoleService, Depends(get_role_service)]):
    roles = await roles_service.get_all()
    return roles


@router.get("/my_role", response_model=Role)
async def get_my_role(roles_service: Annotated[RoleService, Depends(get_role_service)]):
    return await roles_service.get_my_role()


@router.get("/{role_id}", response_model=Role)
async def get_role(
    roles_service: Annotated[RoleService, Depends(get_role_service)], role_id: int
):
    return await roles_service.get(role_id)


@router.patch("/{role_id}", response_model=Role)
async def update_role(
    roles_service: Annotated[RoleService, Depends(get_role_service)],
    role_id: int,
    new_data: UpdateRole,
):
    return await roles_service.update(role_id, new_data)


@router.delete("/{role_id}", status_code=204)
async def delete_role(
    roles_service: Annotated[RoleService, Depends(get_role_service)], role_id: int
):
    await roles_service.delete(role_id)
