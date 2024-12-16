from unittest.mock import AsyncMock, patch

import pytest

from microsoft.app.activity.entities import ActivityIn
from microsoft.app.activity.service import create_activity_service
from microsoft.app.exceptions import MicrosoftException
from microsoft.app.repositories.activities.create_activity import Activity


@pytest.mark.asyncio
@patch(
    "microsoft.app.repositories.activities.create_activity.PersistActivityRepository"
)
async def test_create_activity_success(mock_repo_class):
    mock_repo = mock_repo_class.return_value
    mock_repo.run = AsyncMock(
        return_value=Activity(
            id="123e4567-e89b-12d3-a456-426614174000",
            name="Design Homepage",
            description="Create homepage layout using Figma",
            project_id="321e6547-e89b-12d3-a456-426614174111",
            created_at="2023-01-01T00:00:00",
        )
    )

    mock_payload = ActivityIn(
        name="Design Homepage",
        description="Create homepage layout using Figma",
        project_id="321e6547-e89b-12d3-a456-426614174111",
    )

    result = await create_activity_service(
        repository=mock_repo,
        payload=mock_payload,
    )

    assert result.name == "Design Homepage"
    assert result.description == "Create homepage layout using Figma"
    assert str(result.project_id) == "321e6547-e89b-12d3-a456-426614174111"


@pytest.mark.asyncio
@patch(
    "microsoft.app.repositories.activities.create_activity.PersistActivityRepository"
)
async def test_create_activity_failed(mock_repo_class):
    mock_repo = mock_repo_class.return_value
    mock_repo.run = AsyncMock(side_effect=Exception("Error to create activity"))

    mock_payload = ActivityIn(
        name="Design Homepage",
        description="Create homepage layout using Figma",
        project_id="321e6547-e89b-12d3-a456-426614174111",
    )

    with pytest.raises(MicrosoftException) as excinfo:
        await create_activity_service(
            repository=mock_repo,
            payload=mock_payload,
        )

    assert excinfo.value.type.value == "CREATE_ACTIVITY_ERROR"
    assert str(excinfo.value) == "Error to create activity"
