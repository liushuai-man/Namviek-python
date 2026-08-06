from dataclasses import dataclass


@dataclass(slots=True)
class AppError(Exception):
    status_code: int
    code: str
    message: str


class AuthenticationError(AppError):
    def __init__(self, message: str = "Invalid email or password") -> None:
        super().__init__(401, "authentication_failed", message)


class AuthorizationError(AppError):
    def __init__(self, message: str = "Authentication is required") -> None:
        super().__init__(401, "not_authenticated", message)


class ConflictError(AppError):
    def __init__(self, message: str) -> None:
        super().__init__(409, "resource_conflict", message)


class RegistrationDisabledError(AppError):
    def __init__(self) -> None:
        super().__init__(403, "registration_disabled", "Registration is disabled")


class UnsupportedAuthProviderError(AppError):
    def __init__(self) -> None:
        super().__init__(400, "unsupported_auth_provider", "Unsupported auth provider")

