import pytest

from src.auth.service import AuthService
from src.infrastructure.config import Settings


@pytest.mark.asyncio
async def test_get_google_redirect_url(
        settings: Settings,
        auth_service: AuthService
):
    settings_google_redirect_url = settings.google_redirect_url
    auth_service_google_redirect_url = auth_service.\
        get_google_redirect_url()
    assert settings_google_redirect_url == auth_service_google_redirect_url


@pytest.mark.asyncio
async def test_generate_access_token(
        auth_service: AuthService
):
    user_id = 1
    access_token = auth_service.generate_access_token(user_id=user_id)
    decoded_user_id = auth_service.get_user_id_from_access_token(
        access_token=access_token
    )

    assert decoded_user_id == user_id


@pytest.mark.asyncio
async def test_google_auth(
        mock_auth_service: AuthService,
):
    await mock_auth_service.google_auth(code="fake code")
