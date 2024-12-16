from datetime import datetime
from typing import AsyncGenerator
from uuid import UUID

from pydantic import BaseModel
from sqlalchemy.exc import IntegrityError

from microsoft.app.exceptions import MicrosoftException, MicrosoftExceptionType
from microsoft.app.models import DBActivity
from microsoft.db.dependency_factory import create_repository
from microsoft.db.repository import BaseRepository


class CreateActivityDataIn(BaseModel):
    name: str
    description: str | None = None
    project_id: UUID


class Activity(BaseModel):
    id: UUID
    name: str
    description: str | None
    project_id: UUID
    created_at: datetime


def create_db_activity(activity: CreateActivityDataIn) -> DBActivity:
    return DBActivity(
        name=activity.name,
        description=activity.description,
        project_id=activity.project_id,
    )


async def to_activity(db_activity: DBActivity) -> Activity:
    return Activity(
        id=db_activity.id,
        name=db_activity.name,
        description=db_activity.description,
        project_id=db_activity.project_id,
        created_at=db_activity.created_at,
    )


class PersistActivityRepository(BaseRepository):
    async def run(self, activity: CreateActivityDataIn) -> Activity:
        try:
            db_activity = create_db_activity(activity)
            self.db_session.add(db_activity)
            await self.db_session.commit()
            await self.db_session.refresh(db_activity)
        except IntegrityError:
            raise MicrosoftException(
                type=MicrosoftExceptionType.ACTIVITY_ALREADY_EXISTS,
                message="Activity already exists in the database",
            )
        except Exception:
            raise MicrosoftException(
                type=MicrosoftExceptionType.CREATE_ACTIVITY_ERROR,
                message="Error to create activity",
            )
        return await to_activity(db_activity)


async def factory() -> AsyncGenerator[PersistActivityRepository, None]:
    async for repository in create_repository(PersistActivityRepository):
        yield repository  # type: ignore
