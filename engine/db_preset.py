import asyncio

from sqlalchemy.exc import PendingRollbackError, IntegrityError

from engine.auth.models import *
from engine.auth.repos.roles_repo import RoleRepository
from engine.auth.repos.user_repo import UserRepository
from engine.auth.schemas.schemes import UserCreate
from engine.auth.services.user_manager import UserManager
from engine.db import async_session_maker, engine
from engine.utils import PasswordHelper


async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def add_role(session, role_name: str):
    try:
        role_repo = RoleRepository(session)
        await role_repo.create({"name": role_name})
    except PendingRollbackError:
        pass
    except IntegrityError:
        pass


async def main():
    await init_models()

    async with async_session_maker() as session:
        await add_role(session, "admin")
        await add_role(session, "camera")
        await add_role(session, "client")

        try:
            manager = UserManager(
                UserRepository(session), RoleRepository(session), PasswordHelper()
            )
            user = UserCreate(username="ondrei", password="a1024lagno", role_id="1")
            await manager.create(user)
        except PendingRollbackError:
            pass
        except IntegrityError:
            pass


def run():
    asyncio.run(main())


if __name__ == "__main__":
    asyncio.run(main())
