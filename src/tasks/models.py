from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from src.infrastructure.db import Base


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