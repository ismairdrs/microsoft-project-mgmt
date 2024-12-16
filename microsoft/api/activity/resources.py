from http import HTTPStatus

from fastapi import APIRouter, Depends

from microsoft.api.activity.schema import ActivityIn, ActivityOut
from microsoft.app.activity.service import create_activity_service
from microsoft.app.repositories.activities.create_activity import (
    PersistActivityRepository,
    factory,
)

router = APIRouter(tags=["activities"])


@router.post(
    "/activities",
    response_model=ActivityOut,
    status_code=HTTPStatus.CREATED,
)
async def register_activity(
    payload: ActivityIn,
    repository: PersistActivityRepository = Depends(factory),
) -> ActivityOut:
    result = await create_activity_service(repository=repository, payload=payload)
    return ActivityOut(
        id=result.id,
        name=result.name,
        description=result.description,
        project_id=result.project_id,
        created_at=result.created_at,
    )
