import pytest

from dataclasses import dataclass

from src.infrastructure.config import settings, Settings
from src.auth.schemas import GoogleUserData


import factory.fuzzy
from faker import Faker
from pytest_factoryboy import register

fake = Faker()


@dataclass
class FakeGoogleClient:
    settings: Settings

    async def get_user_info(self, code: str) -> GoogleUserData:
        return GoogleUserData(
            id=fake.random_int(),  # Не LazyFunction, а сразу значение
            name=fake.name(),
            access_token=fake.sha256(),
            email=fake.email(),
            email_verified=True
        )

    @staticmethod
    async def _get_user_access_token(code: str) -> str:
        return f"fake_access_token {code}"


@pytest.fixture
def google_client():
    return FakeGoogleClient(settings=settings)


@pytest.fixture
def google_user_info_data() -> GoogleUserData:
    return GoogleUserData(
        id=factory.LazyFunction(lambda: fake.random_int()),
        name=factory.LazyFunction(lambda: fake.name()),
        access_token=factory.LazyFunction(lambda: fake.sha256()),
        email=factory.LazyFunction(lambda: fake.email()),
        email_verified=True
    )
