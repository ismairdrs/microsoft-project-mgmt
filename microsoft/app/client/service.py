from microsoft.api.clients.schema import ClientIn
from microsoft.app.exceptions import MicrosoftException, MicrosoftExceptionType
from microsoft.app.repositories.clients.create_client import (
    Client,
    CreateClientDataIn,
    PersistClientRepository,
)


def to_create_client_data_in(payload: ClientIn) -> CreateClientDataIn:
    return CreateClientDataIn(
        name=payload.name, email=payload.email, phone=payload.phone
    )


async def create_client_service(
    repository: PersistClientRepository, payload: ClientIn
) -> Client:
    try:
        client = to_create_client_data_in(payload)
        return await repository.run(client=client)
    except MicrosoftException as e:
        raise e
    except Exception:
        raise MicrosoftException(
            type=MicrosoftExceptionType.CREATE_CLIENT_ERROR,
            message="Error to create client",
        )
