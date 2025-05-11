from sqlalchemy.orm import Session
from sqlalchemy import insert, select

from dataclasses import dataclass
from db.models import UserModel


@dataclass
class UserRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def create_user(self,
                    username: str,
                    password: str
                    ) -> UserModel:
        query = insert(UserModel).values(
            username=username,
            password=password
        ).returning(UserModel.id)
        with self.db_session as session:
            user_id: int = session.execute(query).scalar()
            session.commit()
            return self.get_user(user_id)

    def get_user(self, user_id) -> UserModel | None:
        query = select(UserModel).where(UserModel.id == user_id)
        with self.db_session as session:
            return session.execute(query).scalar_one_or_none()

    def get_user_by_username(self, username: str) -> UserModel | None:
        query = select(UserModel).where(UserModel.username == username)
        with self.db_session as session:
            return session.execute(query).scalar_one_or_none()
