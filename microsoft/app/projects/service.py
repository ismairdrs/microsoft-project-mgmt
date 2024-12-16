from microsoft.app.exceptions import MicrosoftException, MicrosoftExceptionType
from microsoft.app.projects.entities import ProjectIn
from microsoft.app.repositories.projects.create_project import PersistProjectRepository


async def create_project_service(
    repository: PersistProjectRepository, payload: ProjectIn
):
    try:
        return await repository.run(project=payload)
    except Exception:
        raise MicrosoftException(
            type=MicrosoftExceptionType.CREATE_PROJECT_ERROR,
            message="Error to create project",
        )
