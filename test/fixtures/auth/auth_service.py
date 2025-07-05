import pytest

from src.infrastructure.config import settings
from src.auth.service import AuthService


@pytest.fixture
def auth_service(user_repository, google_client):
    return AuthService(
        user_repository=user_repository,
        settings=settings,
        google_client=google_client
    )
