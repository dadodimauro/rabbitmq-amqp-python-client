from datetime import datetime, timedelta
from typing import AsyncGenerator

import pytest_asyncio

from rabbitmq_amqp_python_client import (
    AsyncConnection,
    AsyncEnvironment,
    OAuth2Options,
    PosixSslConfigurationContext,
    RecoveryConfiguration,
    WinSslConfigurationContext,
)

from ..utils import token


@pytest_asyncio.fixture
async def async_environment():
    """Fixture for async environment."""
    environment = AsyncEnvironment(uri="amqp://guest:guest@localhost:5672/")
    yield environment
    await environment.close()


@pytest_asyncio.fixture
async def environment_auth() -> AsyncGenerator[AsyncEnvironment, None]:
    token_string = token(datetime.now() + timedelta(milliseconds=2500))
    environment = AsyncEnvironment(
        uri="amqp://localhost:5672",
        oauth2_options=OAuth2Options(token=token_string),
    )
    yield environment
    await environment.close()


@pytest_asyncio.fixture
async def async_connection() -> AsyncGenerator[AsyncConnection, None]:
    environment = AsyncEnvironment(
        uri="amqp://guest:guest@localhost:5672/",
    )
    connection = await environment.connection()
    await connection.dial()
    yield connection
    await connection.close()


@pytest_asyncio.fixture
async def async_connection_with_reconnect() -> AsyncGenerator[AsyncConnection, None]:
    """Fixture providing an async connection with recovery enabled."""
    environment = AsyncEnvironment(
        uri="amqp://guest:guest@localhost:5672/",
        recovery_configuration=RecoveryConfiguration(active_recovery=True),
    )
    connection = await environment.connection()
    await connection.dial()
    yield connection
    await connection.close()


@pytest_asyncio.fixture
async def async_connection_ssl(
    ssl_context: PosixSslConfigurationContext | WinSslConfigurationContext,
) -> AsyncGenerator[AsyncConnection, None]:
    environment = AsyncEnvironment(
        uri="amqps://guest:guest@localhost:5671/",
        ssl_context=ssl_context,
    )
    connection = await environment.connection()
    await connection.dial()
    yield connection
    await connection.close()
