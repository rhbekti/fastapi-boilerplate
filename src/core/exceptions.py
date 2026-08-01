from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
import logging

logger = logging.getLogger(__name__)


class AlreadyExistsError(Exception):
    """Exception raised when a resource already exists."""

    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


async def already_exists_exception_handler(
    request: Request, exc: AlreadyExistsError
) -> JSONResponse:
    return JSONResponse(
        status_code=409,
        content={"success": False, "message": exc.message, "data": None},
    )


async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"success": False, "message": exc.detail, "data": None},
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={"success": False, "message": exc.errors(), "data": None},
    )


async def unhandled_exception_handler(request: Request, exc: Exception):
    logger.exception("Unhandled exception occurred")
    return JSONResponse(
        status_code=500,
        content={"success": False, "message": "Internal server error", "data": None},
    )


def setup_exception_handlers(app: FastAPI):
    app.add_exception_handler(AlreadyExistsError, already_exists_exception_handler)
    app.add_exception_handler(StarletteHTTPException, http_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(Exception, unhandled_exception_handler)
