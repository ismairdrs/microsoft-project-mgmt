import threading
from typing import Callable

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

import settings

_engines = {}
_session_factories = {}
_is_single_threaded: bool = False
_engine: AsyncEngine
_session_factory: Callable


def create_thread_safe_context(is_single_threaded: bool = False) -> None:
    engine = create_async_engine(
        settings.build_database_uri(), **settings.retrieve_engine_config()
    )
    async_session_factory = async_sessionmaker(bind=engine, **settings.build_session_config())  # type: ignore  # noqa
    if is_single_threaded:
        global _is_single_threaded, _engine, _session_factory
        _is_single_threaded = is_single_threaded
        _engine = engine
        _session_factory = async_session_factory
    else:
        thread_id = threading.get_native_id()
        _engines.update({thread_id: engine})
        _session_factories.update({thread_id: async_session_factory})


def get_threaded_engine() -> AsyncEngine:
    global _is_single_threaded
    if _is_single_threaded:
        return _engine
    return _engines[threading.get_native_id()]  # pragma: no cover


def create_threaded_session() -> AsyncSession:
    global _is_single_threaded, _session_factory
    if _is_single_threaded:
        return _session_factory()
    return _session_factories[threading.get_native_id()]()  # pragma: no cover


async def teardown_thread_safe_context() -> None:
    global _is_single_threaded, _engine
    if _is_single_threaded:
        return await _engine.dispose(close=True)  # type: ignore
    await _engines[threading.get_native_id()].dispose(close=True)  # pragma: no cover
    _engines.pop(threading.get_native_id(), None)  # pragma: no cover
