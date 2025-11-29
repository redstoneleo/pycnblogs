"""Exception classes for pycnblogs."""


class CnblogsError(Exception):
    """Base exception for all pycnblogs errors."""
    pass


class AuthenticationError(CnblogsError):
    """Raised when authentication fails."""
    pass


class APIError(CnblogsError):
    """Raised when API request fails."""
    
    def __init__(self, message: str, status_code: int = None):
        super().__init__(message)
        self.status_code = status_code
        self.message = message
