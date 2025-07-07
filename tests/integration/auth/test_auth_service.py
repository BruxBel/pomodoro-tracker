import pytest


@pytest.mark.asyncio
async def test_google_auth(auth_service):
    code = "fake_code"
    user = await auth_service.google_auth(code)
    assert user is not None
