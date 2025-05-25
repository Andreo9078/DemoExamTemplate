from typing import Literal

from ..domain import User, Role
from ..exceptions import RoleDoesNotExist, RoleAlreadyExists
from ..repos.roles_repo import RoleRepository
from ..schemas.schemes import CreateRole, UpdateRole
from engine.exceptions import PermissionDenied


class RoleService:
    def __init__(
        self,
        role_repo: RoleRepository,
        curr_user: User,
    ):
        self.role_repo = role_repo
        self.current_user = curr_user

    async def create(self, role_create: CreateRole) -> Role:
        self._check_perm("create")

        role = await self.role_repo.get_by_name(role_create.name)
        if role is not None:
            raise RoleAlreadyExists(role_create.name)

        created_role = await self.role_repo.create(role_create.model_dump())
        return created_role

    async def get(self, id_: int) -> Role:
        self._check_perm("get")

        role = await self.role_repo.get(id_)
        if role is None:
            raise RoleDoesNotExist(id_)
        return role

    async def get_my_role(self) -> Role:
        self._check_perm("get")

        return self.current_user.role

    async def get_all(self) -> list[Role]:
        self._check_perm("get")

        roles = await self.role_repo.get_all()
        return roles

    async def update(self, id_: int, update_role: UpdateRole):
        self._check_perm("update")

        role = await self.role_repo.get(id_)
        if role is None:
            raise RoleDoesNotExist(id_)
        updated_role = await self.role_repo.update(role.id, update_role.model_dump())

        return updated_role

    async def delete(self, id_: int) -> Role:
        self._check_perm("delete")

        role = await self.role_repo.get(id_)

        if role is None:
            raise RoleDoesNotExist(id_)

        await self.role_repo.delete(role.id)
        return role

    def _check_perm(self, action: Literal["get", "update", "create", "delete"]):
        if self.current_user.role.name != "admin" and action != "get":
            raise PermissionDenied
