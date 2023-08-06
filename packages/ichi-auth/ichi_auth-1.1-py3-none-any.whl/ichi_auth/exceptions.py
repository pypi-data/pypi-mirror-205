class AuthJWTException(Exception):
    """
    Base except which all fastapi_jwt_auth errors extend
    """

    def __init__(self, status_code: int, message: str, _error_code: str = ""):
        self.status_code = status_code
        self.message = message
        if _error_code:
            self.error_code = _error_code


class InvalidHeaderError(AuthJWTException):
    """
    An error getting jwt in header or jwt header information from a request
    """

    error_code = "invalid_header"


class JWTDecodeError(AuthJWTException):
    """
    An error decoding a JWT
    """

    error_code = "token_decode_failed"


class CSRFError(AuthJWTException):
    """
    An error with CSRF protection
    """

    error_code = "csrf_error"


class MissingTokenError(AuthJWTException):
    """
    Error raised when token not found
    """

    error_code = "missing_token"


class RevokedTokenError(AuthJWTException):
    """
    Error raised when a revoked token attempt to access a protected endpoint
    """

    error_code = "revoked_token"


class AccessTokenRequired(AuthJWTException):
    """
    Error raised when a valid, non-access JWT attempt to access an endpoint
    protected by jwt_required, jwt_optional, fresh_jwt_required
    """

    error_code = "access_token_required"


class RefreshTokenRequired(AuthJWTException):
    """
    Error raised when a valid, non-refresh JWT attempt to access an endpoint
    protected by jwt_refresh_token_required
    """

    error_code = "refresh_token_required"


class FreshTokenRequired(AuthJWTException):
    """
    Error raised when a valid, non-fresh JWT attempt to access an endpoint
    protected by fresh_jwt_required
    """

    error_code = "fresh_token_required"
