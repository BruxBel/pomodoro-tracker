from typing import Any, Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import (Mapped, DeclarativeBase, mapped_column,
                            declared_attr)


class Base(DeclarativeBase):
    id: Any
    __name__ = str

    __allow_unmapped__ = True

    @declared_attr
    def __tablename__(self) -> str:
        return self.__name__.lower()


class TaskModel(Base):
    __tablename__ = "Tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    pomodoro_count: Mapped[int]
    category_id: Mapped[int]
    user_id: Mapped[int] = mapped_column(ForeignKey("Users.id"),
                                         nullable=False)


class CategoryModel(Base):
    __tablename__ = "Categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]


class UserModel(Base):
    __tablename__ = "Users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
