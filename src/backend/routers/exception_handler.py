import logging

from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException, RequestValidationError
from pydantic import BaseModel

from backend.exceptions import AlreadyExists, NotFound

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


async def exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Catch Exception and crete response with appropriate status code and body.
    :param request:
    :param exc:
    :return:
    """
    if isinstance(exc, AlreadyExists):
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={"message": exc.message},
        )
    elif isinstance(exc, NotFound):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": exc.message},
        )
    else:
        logger.error("Unhandled %s:", type(exc).__name__, exc_info=exc)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": "Internal server error"},
        )
    # if isinstance(exc, RequestValidationError):
    #     return JSONResponse(
    #         status_code=status.HTTP_422, content={"errors": {"password": "too short", "email": "nor right email format"}})



