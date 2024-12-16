from datetime import datetime
from typing import AsyncGenerator
from uuid import UUID

from pydantic import BaseModel
from sqlalchemy.exc import IntegrityError

from microsoft.app.exceptions import MicrosoftException, MicrosoftExceptionType
from microsoft.app.models import DBProject
from microsoft.db.dependency_factory import create_repository
from microsoft.db.repository import BaseRepository
from microsoft.enums import ProjectStatus


class CreateProjectDataIn(BaseModel):
    name: str
    status: ProjectStatus = ProjectStatus.OPEN
    client_id: UUID
    description: str | None = None


class Project(BaseModel):
    id: UUID
    name: str
    description: str | None
    status: ProjectStatus
    client_id: UUID
    created_at: datetime


def create_db_project(project: CreateProjectDataIn) -> DBProject:
    return DBProject(
        name=project.name,
        description=project.description,
        status=ProjectStatus.OPEN,
        client_id=project.client_id,
    )


async def to_project(db_project: DBProject) -> Project:
    return Project(
        id=db_project.id,
        name=db_project.name,
        description=db_project.description,
        status=db_project.status,
        client_id=db_project.client_id,
        created_at=db_project.created_at,
    )


class PersistProjectRepository(BaseRepository):
    async def run(self, project: CreateProjectDataIn) -> Project:
        try:
            db_project = create_db_project(project)
            self.db_session.add(db_project)
            await self.db_session.commit()
            await self.db_session.refresh(db_project)
        except IntegrityError:
            raise MicrosoftException(
                type=MicrosoftExceptionType.PROJECT_ALREADY_EXISTS,
                message="Project already exists in the database",
            )
        except Exception:
            raise MicrosoftException(
                type=MicrosoftExceptionType.CREATE_PROJECT_ERROR,
                message="Error to create project",
            )
        return await to_project(db_project)


async def factory() -> AsyncGenerator[PersistProjectRepository, None]:
    async for repository in create_repository(PersistProjectRepository):
        yield repository  # type: ignore
