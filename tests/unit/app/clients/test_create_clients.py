from unittest.mock import AsyncMock, patch

import pytest

from microsoft.app.client.entities import ClientIn
from microsoft.app.client.service import create_client_service
from microsoft.app.exceptions import MicrosoftException
from microsoft.app.repositories.clients.create_client import (
    PersistClientRepository,
    Client,
)


@pytest.mark.asyncio
@patch("microsoft.app.repositories.clients.create_client.PersistClientRepository")
async def test_create_client_success(mock_repo_class):
    mock_repo = mock_repo_class.return_value
    mock_repo.run = AsyncMock(
        return_value=Client(
            id="123e4567-e89b-12d3-a456-426614174000",
            name="Ismair Junior",
            email="test@gmail.com",
            phone="62981888888",
            created_at="2023-01-01T00:00:00",
        )
    )

    mock_payload = ClientIn(
        name="Ismair Junior",
        email="test@gmail.com",
        phone="62981888888",
    )

    result = await create_client_service(
        repository=mock_repo,
        payload=mock_payload,
    )

    assert result.name == "Ismair Junior"
    assert result.email == "test@gmail.com"
    assert result.phone == "62981888888"


@pytest.mark.asyncio
@patch("microsoft.app.repositories.clients.create_client.PersistClientRepository")
async def test_create_client_failed(mock_repo_class):
    mock_repo = mock_repo_class.return_value
    mock_repo.run = AsyncMock(side_effect=Exception("Error to create client"))

    mock_payload = ClientIn(
        name="Ismair Junior",
        email="test@gmail.com",
        phone="62981888888",
    )

    with pytest.raises(MicrosoftException) as excinfo:
        await create_client_service(
            repository=mock_repo,
            payload=mock_payload,
        )

    assert excinfo.value.type.value == "CREATE_CLIENT_ERROR"
    assert str(excinfo.value) == "Error to create client"
