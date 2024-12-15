from microsoft.app.repositories.clients.create_client import (
    Client,
    PersistClientRepository,
)
from microsoft.app.client.entities import ClientIn


async def create_client_service(
    repository: PersistClientRepository, payload: ClientIn
) -> Client:
    try:
        return await repository.run(client=payload)
    except Exception as e:
        print(f'Expcetion: {e}')
        # raise NotImplemented("Gravar logs e lanaçar exception correta")
