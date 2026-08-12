from collections.abc import Awaitable, Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware


class CorsMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, allow_origins: list[str]) -> None:
        super().__init__(app)
        self.allow_origins = allow_origins

    def _is_origin_allowed(self, origin: str | None) -> bool:
        if not origin:
            return False
        if origin in self.allow_origins:
            return True
        return any(origin.startswith(pattern) for pattern in self.allow_origins)

    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        origin = request.headers.get("origin")

        if request.method == "OPTIONS" and origin:
            if self._is_origin_allowed(origin):
                response = Response(status_code=204)
                response.headers["Access-Control-Allow-Origin"] = origin
                response.headers["Access-Control-Allow-Credentials"] = "true"
                response.headers["Access-Control-Allow-Methods"] = (
                    "GET, POST, PUT, DELETE, PATCH, OPTIONS"
                )
                response.headers["Access-Control-Allow-Headers"] = (
                    "Content-Type, Authorization, RefreshToken, "
                    "X-Requested-With, Accept, Origin"
                )
                response.headers["Access-Control-Max-Age"] = "86400"
                return response
            return Response(status_code=403)

        response = await call_next(request)

        if origin and self._is_origin_allowed(origin):
            response.headers["Access-Control-Allow-Origin"] = origin
            response.headers["Access-Control-Allow-Credentials"] = "true"
            response.headers["Access-Control-Expose-Headers"] = (
                "Authorization, RefreshToken"
            )

        return response


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        return response
