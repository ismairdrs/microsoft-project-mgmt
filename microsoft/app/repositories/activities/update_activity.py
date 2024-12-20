from datetime import datetime
from typing import AsyncGenerator
from uuid import UUID

from pydantic import BaseModel
from sqlalchemy.exc import IntegrityError

from microsoft.app.exceptions import MicrosoftException, MicrosoftExceptionType
from microsoft.app.models import DBActivity
from microsoft.db.dependency_factory import create_repository
from microsoft.db.repository import BaseRepository


class UpdateActivityDataIn(BaseModel):
    name: str | None = None
    description: str | None = None
    project_id: UUID | None = None


class Activity(BaseModel):
    id: UUID
    name: str
    description: str | None
    project_id: UUID
    completed: bool
    created_at: datetime
    updated_at: datetime | None


async def update_db_activity(
    db_activity: DBActivity, updates: UpdateActivityDataIn
) -> DBActivity:
    if updates.name is not None:
        db_activity.name = updates.name
    if updates.description is not None:
        db_activity.description = updates.description
    if updates.completed is not None:
        db_activity.completed = updates.completed
    db_activity.updated_at = datetime.utcnow()
    return db_activity


async def to_activity(db_activity: DBActivity) -> Activity:
    return Activity(
        id=db_activity.id,
        name=db_activity.name,
        description=db_activity.description,
        project_id=db_activity.project_id,
        completed=db_activity.completed,
        created_at=db_activity.created_at,
        updated_at=db_activity.updated_at,
    )


class UpdateActivityRepository(BaseRepository):
    async def run(self, activity_id: UUID, updates: UpdateActivityDataIn) -> Activity:
        db_activity = await self.db_session.get(DBActivity, activity_id)
        if not db_activity:
            raise MicrosoftException(
                type=MicrosoftExceptionType.ACTIVITY_NOT_FOUND,
                message=f"Activity with ID {activity_id} not found",
            )
        try:
            updated_activity = await update_db_activity(db_activity, updates)  # type: ignore
            await self.db_session.commit()
            await self.db_session.refresh(updated_activity)
        except IntegrityError:
            raise MicrosoftException(
                type=MicrosoftExceptionType.UPDATE_ACTIVITY_ERROR,
                message="Integrity error during activity update",
            )
        except Exception:
            raise MicrosoftException(
                type=MicrosoftExceptionType.UPDATE_ACTIVITY_ERROR,
                message="Error updating activity",
            )
        return await to_activity(updated_activity)


async def factory() -> AsyncGenerator[UpdateActivityRepository, None]:
    async for repository in create_repository(UpdateActivityRepository):
        yield repository  # type: ignore
