import pytest
import pytest_asyncio

from src.auth.service import AuthService
from src.users.repository import UserRepository


@pytest.fixture
def mock_auth_service(settings, fake_user_repository, google_client):
    return AuthService(
        user_repository=fake_user_repository,
        settings=settings,
        google_client=google_client
    )


@pytest_asyncio.fixture
async def auth_service(settings, get_db_session, google_client):
    # Создаем сервис с сессией, но не управляем сессией здесь
    return AuthService(
        user_repository=UserRepository(db_session=get_db_session),
        settings=settings,
        google_client=google_client
    )
