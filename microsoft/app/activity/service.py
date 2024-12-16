from microsoft.app.activity.entities import ActivityIn
from microsoft.app.exceptions import MicrosoftException, MicrosoftExceptionType
from microsoft.app.repositories.activities.create_activity import (
    PersistActivityRepository,
)


async def create_activity_service(
    repository: PersistActivityRepository, payload: ActivityIn
):
    try:
        return await repository.run(activity=payload)
    except Exception:
        raise MicrosoftException(
            type=MicrosoftExceptionType.CREATE_ACTIVITY_ERROR,
            message="Error to create activity",
        )
