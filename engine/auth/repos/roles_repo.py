from typing import Optional, Annotated

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..domain import Role
from ..models import RoleORMModel
from engine.base import NewSQLAlchemyRepository
from engine.db import get_async_session


class RoleRepository(NewSQLAlchemyRepository[Role, RoleORMModel, int]):
    def __init__(self, session: AsyncSession):
        super().__init__(Role, RoleORMModel, session)

    async def get_by_name(self, name: str) -> Optional[Role]:
        stmt = select(RoleORMModel).where(RoleORMModel.name == name)

        res = (await self.session.execute(stmt)).scalar_one_or_none()

        if res is None:
            return None

        return self.domain_obj.model_validate(res)


async def get_role_repository(
    session: Annotated[AsyncSession, Depends(get_async_session)],
) -> RoleRepository:
    return RoleRepository(session)
