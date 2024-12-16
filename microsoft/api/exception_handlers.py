from http import HTTPStatus
from json import JSONDecodeError
from typing import Union

from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse

from microsoft.app.exceptions import MicrosoftException

from .response_handlers import (
    error_to_response,
    http_exception_to_response,
    json_decode_to_response,
)


async def validation_exception_handler(
    request: Request, exc: Union[MicrosoftException]
) -> JSONResponse:
    body = error_to_response(exc)
    return JSONResponse(status_code=body.code, content=body.model_dump())


async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    body = http_exception_to_response(exc)
    return JSONResponse(status_code=body.code, content=body.model_dump())


async def bad_request_handler(
    request: Request,
    exc: JSONDecodeError,
) -> JSONResponse:
    body = json_decode_to_response(exc)
    return JSONResponse(status_code=body.code, content=body.model_dump())


async def not_implemented_handler(
    request: Request, exc: NotImplementedError
) -> JSONResponse:
    return JSONResponse(
        status_code=HTTPStatus.NOT_IMPLEMENTED, content={"message": str(exc)}
    )
