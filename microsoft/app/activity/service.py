from microsoft.api.activity.schema import ActivityIn
from microsoft.app.exceptions import MicrosoftException, MicrosoftExceptionType
from microsoft.app.repositories.activities.create_activity import (
    Activity,
    CreateActivityDataIn,
    PersistActivityRepository,
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
