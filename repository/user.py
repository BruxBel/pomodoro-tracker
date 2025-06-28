from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select

from dataclasses import dataclass
from db.models import UserModel
from schemas import UserCreateSchema


@dataclass
class UserRepository:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_user_by_email(self, email: str) -> UserModel | None:
        query = select(UserModel).where(UserModel.email == email)
        async with self.db_session as session:
            result = await session.execute(query)
            return result.scalar_one_or_none()

    async def create_user(self, user: UserCreateSchema) -> UserModel:
        query = (
            insert(UserModel)
            .values(**user.model_dump())
            .returning(UserModel.id)
        )
        async with self.db_session as session:
            user_id: int = (await session.execute(query)).scalar()
            await session.commit()
            return await self.get_user(user_id)

    async def get_user(self, user_id: int) -> UserModel | None:
        query = select(UserModel).where(UserModel.id == user_id)
        async with self.db_session as session:
            result = await session.execute(query)
            return result.scalar_one_or_none()

    async def get_user_by_username(self, username: str) -> UserModel | None:
        query = select(UserModel).where(UserModel.username == username)
        async with self.db_session as session:
            result = await session.execute(query)
            return result.scalar_one_or_none()
