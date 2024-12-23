from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter, Depends

from microsoft.api.activity.schema import ActivityIn, ActivityOut, ActivityUpdateIn
from microsoft.app.activity.service import (
    create_activity_service,
    update_activity_service,
)
from microsoft.app.repositories.activities.create_activity import (
    PersistActivityRepository,
    factory,
)
from microsoft.app.repositories.activities.update_activity import (
    UpdateActivityRepository,
)
from microsoft.app.repositories.activities.update_activity import (
    factory as update_activity_factory,
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


@router.patch(
    "/activities/{activity_id}",
    response_model=ActivityOut,
    status_code=HTTPStatus.OK,
)
async def update_activity(
    activity_id: UUID,
    payload: ActivityUpdateIn,
    repository: UpdateActivityRepository = Depends(update_activity_factory),
) -> ActivityOut:
    result = await update_activity_service(
        repository=repository,
        activity_id=activity_id,
        payload=payload,
    )
    return ActivityOut(**result.dict())
