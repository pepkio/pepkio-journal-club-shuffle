from typing import Any, Optional


class PepkioError(Exception):
    """Base exception class for Pepkio SDK errors."""

    pass


class PepkioAPIError(PepkioError):
    """Exception raised when API request fails or returns an error payload."""

    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        response_body: Optional[Any] = None,
    ):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.response_body = response_body

    def __str__(self) -> str:
        if self.status_code:
            return f"[HTTP {self.status_code}] {self.message}"
        return self.message


class PepkioAuthError(PepkioAPIError):
    """Exception raised when authentication fails (401/403)."""

    pass


class PepkioNotFoundError(PepkioAPIError):
    """Exception raised when requested resource is not found (404)."""

    pass
