import asyncio

import pytest

pytest_plugins = [
    "tests.fixtures.auth.auth_service",
    "tests.fixtures.auth.clients",
    "tests.fixtures.users.user_repository",
    "tests.fixtures.infrastructure.settings",
    "tests.fixtures.infrastructure.db",
    # "test.fixtures.users.user_model"
]
