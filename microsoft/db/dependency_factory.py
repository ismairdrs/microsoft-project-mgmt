from typing import AsyncGenerator, Type

from microsoft.db.repository import BaseRepository
from microsoft.db.session_factory import get_pristine_session


async def create_repository(
    RepositoryClass: Type[BaseRepository],
) -> AsyncGenerator[BaseRepository, None]:
    session = get_pristine_session()
    try:
        yield RepositoryClass(session)
    finally:
        await session.close()
