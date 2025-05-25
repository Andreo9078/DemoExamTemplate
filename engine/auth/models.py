from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from engine.db import Base


class UserORMModel(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(
        String(length=320), unique=True, index=True, nullable=False
    )
    hashed_password: Mapped[str] = mapped_column(String(length=1024), nullable=False)
    role_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("roles.id"), nullable=False
    )

    role: Mapped["RoleORMModel"] = relationship("RoleORMModel", lazy="joined")

    is_active: bool = True
    is_superuser: bool = True
    is_verified: bool = True


class RoleORMModel(Base):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    name: Mapped[str] = mapped_column(String(length=320), unique=True, nullable=False)


class CameraOwnerORMModel(Base):
    __tablename__ = "camera_owner"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    owner_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=False
    )
    camera_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=False
    )
