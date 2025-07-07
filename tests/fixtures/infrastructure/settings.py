import pytest
from src.infrastructure.config import Settings


@pytest.fixture()
def settings():
    return Settings()
