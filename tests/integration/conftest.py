import threading

import pytest_asyncio
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

import settings
from microsoft.app.models import DBClient
from microsoft.db.connection import (
    _engines,
    _session_factories,
    create_threaded_session,
)

thread_id = threading.get_native_id()
threaded_engine = create_async_engine(
    settings.build_database_uri(), **settings.retrieve_engine_config()
)
_engines.update({thread_id: threaded_engine})
async_threaded_session_factory = async_sessionmaker(
    bind=threaded_engine, **settings.build_session_config()
)  # type: ignore  # noqa
_session_factories.update({thread_id: async_threaded_session_factory})


@pytest_asyncio.fixture(scope="function")
async def db(override_async_session):
    yield override_async_session


@pytest_asyncio.fixture(scope="function", autouse=True)
async def clean_db(db):
    await db.execute(delete(DBClient))

    await db.commit()


@pytest_asyncio.fixture()
async def override_async_session():
    session = create_threaded_session()
    try:
        yield session
        await session.commit()
    finally:
        await session.close()
