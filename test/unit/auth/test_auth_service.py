import pytest
from jose import jwt

from src.auth.service import AuthService
from src.infrastructure.config import settings


@pytest.mark.asyncio
async def test_get_google_redirect_url(
        auth_service: AuthService,
):
    settings_google_redirect_url = settings.google_redirect_url
    auth_service_google_redirect_url = auth_service.get_google_redirect_url()
    assert settings_google_redirect_url == auth_service_google_redirect_url


@pytest.mark.asyncio
async def test_generate_access_token(
        auth_service: AuthService
):
    user_id = "1"
    access_token = jwt.encode(
        claims={
            'user_id': user_id,
        },
        key=settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ENCODE_ALGORITHM
    )
    payload = jwt.decode(
        token=access_token,
        key=settings.JWT_SECRET_KEY,
        algorithms=[settings.JWT_ENCODE_ALGORITHM]
    )
    decoded_user_id = payload["user_id"]

    assert decoded_user_id == user_id


@pytest.mark.asyncio
async def test_google_auth(
        auth_service: AuthService,
):
    await auth_service.google_auth(code="fake code")
