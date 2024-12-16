from unittest.mock import AsyncMock, patch

import pytest

from microsoft.app.exceptions import MicrosoftException
from microsoft.app.projects.entities import ProjectIn
from microsoft.app.projects.service import create_project_service
from microsoft.app.repositories.projects.create_project import Project


@pytest.mark.asyncio
@patch("microsoft.app.repositories.projects.create_project.PersistProjectRepository")
async def test_create_project_success(mock_repo_class):
    mock_repo = mock_repo_class.return_value
    mock_repo.run = AsyncMock(
        return_value=Project(
            id="123e4567-e89b-12d3-a456-426614174000",
            name="Website Development",
            description="Develop a responsive website",
            status="OPEN",
            client_id="321e6547-e89b-12d3-a456-426614174111",
            created_at="2023-01-01T00:00:00",
        )
    )

    mock_payload = ProjectIn(
        name="Website Development",
        description="Develop a responsive website",
        status="OPEN",
        client_id="321e6547-e89b-12d3-a456-426614174111",
    )

    result = await create_project_service(
        repository=mock_repo,
        payload=mock_payload,
    )

    assert result.name == "Website Development"
    assert result.description == "Develop a responsive website"
    assert result.status == "OPEN"
    assert str(result.client_id) == "321e6547-e89b-12d3-a456-426614174111"


@pytest.mark.asyncio
@patch("microsoft.app.repositories.projects.create_project.PersistProjectRepository")
async def test_create_project_failed(mock_repo_class):
    mock_repo = mock_repo_class.return_value
    mock_repo.run = AsyncMock(side_effect=Exception("Error to create project"))

    mock_payload = ProjectIn(
        name="Website Development",
        description="Develop a responsive website",
        status="OPEN",
        client_id="321e6547-e89b-12d3-a456-426614174111",
    )

    with pytest.raises(MicrosoftException) as excinfo:
        await create_project_service(
            repository=mock_repo,
            payload=mock_payload,
        )

    assert excinfo.value.type.value == "CREATE_PROJECT_ERROR"
    assert str(excinfo.value) == "Error to create project"
