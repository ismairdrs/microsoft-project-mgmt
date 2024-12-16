from http import HTTPStatus

from fastapi import APIRouter, Depends

from microsoft.api.projects.schema import ProjectIn, ProjectOut
from microsoft.app.projects.service import create_project_service
from microsoft.app.repositories.projects.create_project import (
    PersistProjectRepository,
    factory as project_repository_factory,
)

router = APIRouter(tags=["projects"])


@router.post(
    "/projects",
    response_model=ProjectOut,
    status_code=HTTPStatus.CREATED,
)
async def register_project(
    payload: ProjectIn,
    repository: PersistProjectRepository = Depends(project_repository_factory),
) -> ProjectOut:
    result = await create_project_service(repository=repository, payload=payload)
    return ProjectOut(
        id=result.id,
        name=result.name,
        description=result.description,
        status=result.status,
        client_id=result.client_id,
        created_at=result.created_at,
    )
