from fastapi import Request
from fastapi.responses import JSONResponse

from app.core.errors import AppError


async def app_error_handler(_request: Request, exception: Exception) -> JSONResponse:
    if not isinstance(exception, AppError):
        raise exception
    return JSONResponse(
        status_code=exception.status_code,
        content={
            "status": exception.status_code,
            "error": {"code": exception.code, "message": exception.message},
        },
    )
