from microsoft.api.projects.schema import ProjectIn
from microsoft.app.exceptions import MicrosoftException, MicrosoftExceptionType
from microsoft.app.repositories.projects.create_project import (
    CreateProjectDataIn,
    PersistProjectRepository,
    Project,
)


def to_create_project_data_in(payload: ProjectIn) -> CreateProjectDataIn:
    return CreateProjectDataIn(
        name=payload.name,
        description=payload.description,
        client_id=payload.client_id,
    )


async def create_project_service(
    repository: PersistProjectRepository, payload: ProjectIn
) -> Project:
    try:
        project = to_create_project_data_in(payload=payload)
        return await repository.run(project=project)
    except Exception:
        raise MicrosoftException(
            type=MicrosoftExceptionType.CREATE_PROJECT_ERROR,
            message="Error to create project",
        )
