from enum import IntEnum, unique

from sqlalchemy import BigInteger, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.postgres.base_entity import BaseEntity


@unique
class UserType(IntEnum):
    ROOT = 0
    ADMIN = 1
    USER = 2


class UserEntity(BaseEntity):
    __tablename__ = "User"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    fullName: Mapped[str] = mapped_column(String(255), nullable=False)
    username: Mapped[str] = mapped_column(
        String(50), unique=True, nullable=False, index=True
    )
    passwordHash: Mapped[str] = mapped_column(String(255), nullable=False)
    userType: Mapped[int] = mapped_column(Integer, default=UserType.USER)
    isActive: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    createdAt: Mapped[int] = mapped_column(BigInteger, nullable=False)
    updatedAt: Mapped[int] = mapped_column(BigInteger, nullable=False)
