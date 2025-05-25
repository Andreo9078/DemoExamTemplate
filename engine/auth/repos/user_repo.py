from typing import Optional, cast, Annotated

from fastapi import Depends
from sqlalchemy import ColumnElement, select, Select
from sqlalchemy.ext.asyncio import AsyncSession

from engine.base import NewSQLAlchemyRepository
from engine.db import get_async_session
from ..domain import User
from ..models import UserORMModel


class UserRepository(NewSQLAlchemyRepository[User, UserORMModel, int]):
    """
    Database adapter for SQLAlchemy.

    :param session: SQLAlchemy session instance.
    """

    def __init__(
        self,
        session: AsyncSession,
    ):
        super().__init__(User, UserORMModel, session)

    async def get_by_username(self, username: str) -> Optional[User]:
        statement = select(self.table).where(
            cast(ColumnElement[bool], self.table.username == username)
        )
        return await self._get_user(statement)

    async def _get_user(self, statement: Select) -> Optional[User]:
        results = await self.session.execute(statement)
        user = results.unique().scalar_one_or_none()

        if user is None:
            return None

        return self.domain_obj.model_validate(user)


async def get_user_repository(
    session: Annotated[AsyncSession, Depends(get_async_session)],
):
    return UserRepository(session)
