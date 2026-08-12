from fastapi import Request
from fastapi.responses import JSONResponse

from app.core.errors import AppError


async def app_error_handler(request: Request, exception: Exception) -> JSONResponse:
    if not isinstance(exception, AppError):
        raise exception

    response = JSONResponse(
        status_code=exception.status_code,
        content={
            "status": exception.status_code,
            "error": {"code": exception.code, "message": exception.message},
        },
    )

    origin = request.headers.get("origin")
    if origin:
        response.headers["Access-Control-Allow-Origin"] = origin
        response.headers["Access-Control-Allow-Credentials"] = "true"
        response.headers["Access-Control-Expose-Headers"] = (
            "Authorization, RefreshToken"
        )

    return response
