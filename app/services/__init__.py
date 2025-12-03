class ServiceError(Exception):
    """Base exception for service layer."""
    pass


class BusinessRuleError(ServiceError):
    """Raised when a business rule is violated (user-facing)."""
    pass


class NotFoundError(ServiceError):
    """Raised when an expected DB object is not found."""
    pass
