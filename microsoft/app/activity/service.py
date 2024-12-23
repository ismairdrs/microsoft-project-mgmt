from uuid import UUID

from microsoft.api.activity.schema import ActivityIn, ActivityUpdateIn
from microsoft.app.exceptions import MicrosoftException, MicrosoftExceptionType
from microsoft.app.repositories.activities.create_activity import (
    Activity,
    CreateActivityDataIn,
    PersistActivityRepository,
)
from microsoft.app.repositories.activities.update_activity import (
    Activity as ActivityUpdate,
)
from microsoft.app.repositories.activities.update_activity import (
    UpdateActivityDataIn,
    UpdateActivityRepository,
)


def to_create_activity_data_in(payload: ActivityIn) -> CreateActivityDataIn:
    return CreateActivityDataIn(
        name=payload.name,
        description=payload.description,
        project_id=payload.project_id,
    )


async def create_activity_service(
    repository: PersistActivityRepository, payload: ActivityIn
) -> Activity:
    try:
        activity = to_create_activity_data_in(payload=payload)
        return await repository.run(activity=activity)
    except Exception:
        raise MicrosoftException(
            type=MicrosoftExceptionType.CREATE_ACTIVITY_ERROR,
            message="Error to create activity",
        )


def to_update_activity_data_in(payload: ActivityUpdateIn) -> UpdateActivityDataIn:
    return UpdateActivityDataIn(
        name=payload.name,
        description=payload.description,
        project_id=payload.project_id,
    )


async def update_activity_service(
    repository: UpdateActivityRepository, activity_id: UUID, payload: ActivityUpdateIn
) -> ActivityUpdate:
    try:
        activity_update = to_update_activity_data_in(payload=payload)
        return await repository.run(activity_id=activity_id, updates=activity_update)
    except MicrosoftException as e:
        raise e
    except Exception:
        raise MicrosoftException(
            type=MicrosoftExceptionType.UPDATE_ACTIVITY_ERROR,
            message="Error updating activity",
        )
