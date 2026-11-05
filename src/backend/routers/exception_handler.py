import logging

from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from backend.exceptions import AlreadyExistsError, NotFoundError

logger = logging.getLogger(__name__)


class ErrorDetails(BaseModel):
    message: str
    code: int


async def custom_request_validation_error_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    errors: dict[str, str] = {}

    for err in exc.errors():
        loc = [str(part) for part in err["loc"] if part not in ("body", "query", "path", "header", "cookie")]
        field = ".".join(loc) or "body"
        errors.setdefault(field, err["msg"])

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        content={"errors": errors},
    )


async def already_exists_exception_handler(request: Request, exc: AlreadyExistsError) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"message": exc.message},
    )


async def not_found_exception_handler(request: Request, exc: NotFoundError) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"message": exc.message},
    )

