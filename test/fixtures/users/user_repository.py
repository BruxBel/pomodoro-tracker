from dataclasses import dataclass

import pytest

from src.users.schemas import UserCreateSchema
from test.fixtures.users.user_model import UserModelFactory


@dataclass
class FakeUserRepository:

    async def get_user_by_email(self, email: str) -> None:
        return None

    async def create_user(self, user_data: UserCreateSchema):
        return UserModelFactory()


@pytest.fixture
def user_repository():
    return FakeUserRepository()
