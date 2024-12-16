from json import JSONDecodeError
from typing import Any, Dict

from fastapi import FastAPI
from fastapi.exceptions import HTTPException

from microsoft.app.exceptions import MicrosoftException
from microsoft.api.clients.resources import router as clients_router
from microsoft.api.projects.resources import router as projects_router
from microsoft.api.activity.resources import router as activities_router
from microsoft.db.connection import (
    create_thread_safe_context,
    teardown_thread_safe_context,
)
import settings

from .exception_handlers import (
    bad_request_handler,
    http_exception_handler,
    not_implemented_handler,
    validation_exception_handler,
)


def create_application() -> FastAPI:
    application = FastAPI()

    create_thread_safe_context(is_single_threaded=True)

    configure_healthcheck(application)
    configure_routes(application)
    configure_exception_handlers(application)

    return application


def configure_routes(application: FastAPI) -> None:
    application.include_router(clients_router)
    application.include_router(projects_router)
    application.include_router(activities_router)


def configure_exception_handlers(application: FastAPI) -> None:
    application.add_exception_handler(NotImplementedError, not_implemented_handler)
    application.add_exception_handler(HTTPException, http_exception_handler)
    application.add_exception_handler(JSONDecodeError, bad_request_handler)
    application.add_exception_handler(MicrosoftException, validation_exception_handler)


def configure_healthcheck(app: FastAPI) -> None:
    @app.get(settings.HEALTHCHECK_ROUTE)
    async def healthcheck() -> Dict[str, Any]:
        return {
            "application": "Microsoft",
            "healthy": True,
            "environment": settings.ENVIRONMENT,
            "commit_sha": settings.COMMIT_SHA,
        }


app = create_application()


@app.on_event("shutdown")
async def shutdown_event() -> None:
    await teardown_thread_safe_context()
