from microsoft.api.clients.schema import ClientIn
from microsoft.app.exceptions import MicrosoftException, MicrosoftExceptionType
from microsoft.app.repositories.clients.create_client import (
    Client,
    CreateClientDataIn,
    PersistClientRepository,
)
from infrastructure import logging

logger = logging.get_logger(__name__)

def to_create_client_data_in(payload: ClientIn) -> CreateClientDataIn:
    return CreateClientDataIn(
        name=payload.name, email=payload.email, phone=payload.phone
    )


async def create_client_service(
    repository: PersistClientRepository, payload: ClientIn
) -> Client:
    bind_logger = logger.bind(
        function="create_client_service",   
    )
    try:
        client = to_create_client_data_in(payload)
        return await repository.run(client=client)
    except MicrosoftException as e:
        bind_logger.info(f"Ocorreu uma MicrosoftException: {str(e)}")
        raise e
    except Exception:
        bind_logger.info(f"Ocorreu uma Exception: {str(e)}")
        raise MicrosoftException(
            type=MicrosoftExceptionType.CREATE_CLIENT_ERROR,
            message="Error to create client",
        )
