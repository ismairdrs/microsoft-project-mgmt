from datetime import datetime
from typing import AsyncGenerator
from uuid import UUID

from pydantic import BaseModel
from sqlalchemy.exc import IntegrityError

from microsoft.app.exceptions import MicrosoftException, MicrosoftExceptionType
from microsoft.app.models import DBClient
from microsoft.db.dependency_factory import create_repository
from microsoft.db.repository import BaseRepository
from infrastructure import logging

logger = logging.get_logger(__name__)


class CreateClientDataIn(BaseModel):
    name: str
    email: str
    phone: str | None = None


class Client(BaseModel):
    id: UUID
    name: str
    email: str
    created_at: datetime
    phone: str | None = None


def create_db_client(client: CreateClientDataIn) -> DBClient:
    return DBClient(name=client.name, email=client.email, phone=client.phone)


async def to_client(db_client: DBClient) -> Client:
    return Client(
        id=db_client.id,
        name=db_client.name,
        email=db_client.email,
        phone=db_client.phone,
        created_at=db_client.created_at,
    )


class PersistClientRepository(BaseRepository):
    async def run(self, client: CreateClientDataIn) -> Client:
        bind_logger = logger.bind(
        function="create_client_service",   
        )
        try:
            db_client = create_db_client(client)
            self.db_session.add(db_client)
            await self.db_session.commit()
            await self.db_session.refresh(db_client)
        except IntegrityError as e:
            bind_logger.error(f"IntegrityError: {str(e)}")
            raise MicrosoftException(
                type=MicrosoftExceptionType.CLIENT_ALREADY_EXISTS,
                message="Client already exists in the database",
            )
        except Exception as e:
            bind_logger.error(f"Exception: {str(e)}")
            raise MicrosoftException(
                type=MicrosoftExceptionType.CREATE_CLIENT_ERROR,
                message="Error to create client",
            )
        return await to_client(db_client)


async def factory() -> AsyncGenerator[PersistClientRepository, None]:
    async for repository in create_repository(PersistClientRepository):
        yield repository  # type: ignore
