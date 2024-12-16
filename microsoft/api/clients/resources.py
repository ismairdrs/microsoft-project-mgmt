from http import HTTPStatus

from fastapi import APIRouter, Depends

from microsoft.api.clients.schema import ClientIn, ClientOut
from microsoft.app.client.service import create_client_service
from microsoft.app.repositories.clients import create_client

router = APIRouter(tags=["clients"])


@router.post(
    "/clients",
    response_model=ClientOut,
    status_code=HTTPStatus.CREATED,
)
async def register_client(
    payload: ClientIn,
    repository: create_client.PersistClientRepository = Depends(create_client.factory),
) -> ClientOut:
    result = await create_client_service(repository=repository, payload=payload)
    return ClientOut(
        id=result.id,
        name=result.name,
        email=result.email,
        phone=result.phone,
        created_at=result.created_at,
    )
