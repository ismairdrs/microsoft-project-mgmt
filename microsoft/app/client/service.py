from microsoft.app.client.entities import ClientIn
from microsoft.app.exceptions import MicrosoftException, MicrosoftExceptionType
from microsoft.app.repositories.clients.create_client import (
    Client,
    PersistClientRepository,
)


async def create_client_service(
    repository: PersistClientRepository, payload: ClientIn
) -> Client:
    try:
        return await repository.run(client=payload)
    except Exception as e:
        raise MicrosoftException(
            type=MicrosoftExceptionType.CREATE_CLIENT_ERROR,
            message="Error to create client",
        )
