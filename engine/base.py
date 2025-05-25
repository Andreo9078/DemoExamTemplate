from abc import ABC, abstractmethod
from typing import Any, Type, Iterable, Callable, Optional

from pydantic import BaseModel
from sqlalchemy import select, Select
from sqlalchemy.ext.asyncio import AsyncSession

from .exceptions import ObjectDoesNotExist


class RepositoryProtocol[Obj, ID](ABC):
    @abstractmethod
    async def get_all(
        self, offset: int = None, limit: int = None, **filters: Any
    ) -> Iterable[Obj]: ...

    @abstractmethod
    async def get(self, id_obj: ID) -> Obj: ...

    @abstractmethod
    async def create(self, create_dict: dict[str, Any]) -> None: ...

    @abstractmethod
    async def delete(self, id_obj: ID) -> None: ...

    @abstractmethod
    async def update(self, obj: Obj, update_dict: dict[str, Any]) -> None: ...


# noinspection PyProtocol
class SQLAlchemyRepository[ORMObj, ID](RepositoryProtocol[ORMObj, ID]):
    def __init__(self, table: Type[ORMObj], session: AsyncSession) -> None:
        self.table = table
        self.session = session

    async def get(self, id_obj: ID) -> ORMObj:
        statement = select(self.table).where(self.table.id == id_obj)
        res = await self.session.execute(statement)
        return res.scalar_one_or_none()

    async def get_all(self, **filters: Any) -> list[ORMObj]:
        stmt = self._create_get_all_stmt(**filters)
        res = await self.session.execute(stmt)
        return list(res.scalars())

    async def create(self, create_dict: dict[str, Any]) -> ORMObj:
        user = self.table(**create_dict)
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def delete(self, obj: ORMObj) -> ORMObj:
        await self.session.delete(obj)
        await self.session.commit()
        return obj

    async def update(self, obj: ORMObj, new_values: dict[str, Any]) -> ORMObj:
        for key, value in new_values.items():
            setattr(obj, key, value)
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    def _create_get_all_stmt(
        self, offset: int = None, limit: int = None, **filters: Any
    ) -> Select:
        stmt = select(self.table).filter_by(**filters)
        if offset is not None:
            stmt = stmt.offset(offset)
        if limit is not None:
            stmt = stmt.limit(limit)

        return stmt


class NewSQLAlchemyRepository[DomainObj: BaseModel, ORMObj, ID](
    RepositoryProtocol[ORMObj, ID]
):
    def __init__(
        self,
        domain_obj: Type[DomainObj] = BaseModel,
        table: Type[ORMObj] = None,
        session: AsyncSession = None,
    ) -> None:
        self.domain_obj = domain_obj
        self.table = table
        self.session = session

    async def get(self, id_obj: ID) -> Optional[DomainObj]:
        res = await self._get_orm_model(id_obj)

        if res is None:
            return None

        return self.domain_obj.model_validate(res)

    async def get_all(self, **filters: Any) -> list[DomainObj]:
        stmt = self._create_get_all_stmt(**filters)
        res = await self.session.execute(stmt)

        return [self.domain_obj.model_validate(scalar) for scalar in res.scalars()]

    async def create(self, create_dict: dict[str, Any]) -> DomainObj:
        obj = await self._create(create_dict)

        await self.session.commit()
        await self.session.refresh(obj)

        return self.domain_obj.model_validate(obj)

    async def delete(self, id_: ID) -> DomainObj:
        obj_to_del = await self._get_orm_model(id_)
        if obj_to_del:
            await self.session.delete(obj_to_del)
            await self.session.commit()
            return self.domain_obj.model_validate(obj_to_del)

        raise ObjectDoesNotExist(self.domain_obj.__name__, id_)

    async def update(self, id_: ID, new_values: dict[str, Any]) -> DomainObj:
        obj = await self._get_orm_model(id_)
        print(obj)
        if obj is None:
            raise ObjectDoesNotExist(self.domain_obj.__name__, id_)

        for key, value in new_values.items():
            setattr(obj, key, value)
        self.session.add(obj)

        await self.session.commit()
        await self.session.refresh(obj)

        return self.domain_obj.model_validate(obj)

    async def _create(self, create_dict: dict[str, Any]):
        obj = self.table(**create_dict)
        self.session.add(obj)
        return obj

    async def _get_orm_model(self, id_obj: ID) -> ORMObj:
        statement = select(self.table).where(self.table.id == id_obj)
        res = await self.session.execute(statement)
        return res.scalar_one_or_none()

    def _create_get_all_stmt(
        self, offset: int = None, limit: int = None, **filters: Any
    ) -> Select:
        stmt = select(self.table).filter_by(**filters)
        if offset is not None:
            stmt = stmt.offset(offset)
        if limit is not None:
            stmt = stmt.limit(limit)

        return stmt


class BaseDataService[ORMObj, ID](ABC):
    @abstractmethod
    async def get(self, id_: ID) -> ORMObj:
        pass

    @abstractmethod
    async def get_all(self, filters: BaseModel = None) -> list[ORMObj]:
        pass

    @abstractmethod
    async def create(self, create_scheme: BaseModel) -> ORMObj:
        pass

    @abstractmethod
    async def update(self, id_: ID, update_scheme: BaseModel) -> ORMObj:
        pass

    @abstractmethod
    async def delete(self, id_: ID) -> ORMObj:
        pass


class BaseStrategyContext[BaseStrategy](ABC):
    _strategy: BaseStrategy

    def __init__(self) -> None:
        self._strategy = None

    def set_strategy(self, strategy: BaseStrategy) -> None:
        self._strategy = strategy


class BaseAuthUnAuthServiceDepends(ABC):
    __call__: Callable
    """
    This class is for selecting a service and injection its dependencies.

    For use this class you need to implement _get_authorized_service_dep and _get_unauthorized_service_dep.

    First for authorized variation, second for unauthorized variation.

    If you only need one variation you should not use this class.

    We use unauthorized variation for internal usage.
    And authorized variation for external usage, in routers for example.

    """

    def __new__(cls, auth: bool):
        instance = super().__new__(cls)
        if auth:
            return instance._get_authorized_service_dep
        else:
            return instance._get_unauthorized_service_dep

    @abstractmethod
    def _get_authorized_service_dep(self, *args: Any, **kwargs: Any):
        pass

    @abstractmethod
    def _get_unauthorized_service_dep(self, *args: Any, **kwargs: Any):
        pass
