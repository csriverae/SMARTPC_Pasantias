"""
Custom exceptions for MesaPass SaaS application
"""
from fastapi import HTTPException, status


class SaaSException(Exception):
    """Base exception for SaaS application"""
    def __init__(self, message: str, status_code: int = 500, error_code: str = None):
        self.message = message
        self.status_code = status_code
        self.error_code = error_code
        super().__init__(self.message)


class AuthenticationError(SaaSException):
    """Raised when authentication fails"""
    def __init__(self, message: str = "Authentication failed"):
        super().__init__(message, status.HTTP_401_UNAUTHORIZED, "AUTH_ERROR")


class AuthorizationError(SaaSException):
    """Raised when user lacks permission"""
    def __init__(self, message: str = "Insufficient permissions"):
        super().__init__(message, status.HTTP_403_FORBIDDEN, "AUTHZ_ERROR")


class ValidationError(SaaSException):
    """Raised when validation fails"""
    def __init__(self, message: str, field: str = None):
        super().__init__(message, status.HTTP_400_BAD_REQUEST, "VALIDATION_ERROR")
        self.field = field


class ResourceNotFoundError(SaaSException):
    """Raised when resource is not found"""
    def __init__(self, resource: str = "Resource", resource_id: str = None):
        message = f"{resource} not found"
        if resource_id:
            message += f" (ID: {resource_id})"
        super().__init__(message, status.HTTP_404_NOT_FOUND, "NOT_FOUND")


class TenantError(SaaSException):
    """Raised when tenant operation fails"""
    def __init__(self, message: str = "Tenant operation failed"):
        super().__init__(message, status.HTTP_400_BAD_REQUEST, "TENANT_ERROR")


class EmailAlreadyExists(SaaSException):
    """Raised when email is already registered"""
    def __init__(self, email: str):
        super().__init__(
            f"Email '{email}' is already registered",
            status.HTTP_409_CONFLICT,
            "EMAIL_EXISTS"
        )


class InvalidCredentials(SaaSException):
    """Raised when login credentials are invalid"""
    def __init__(self):
        super().__init__(
            "Invalid email or password",
            status.HTTP_401_UNAUTHORIZED,
            "INVALID_CREDENTIALS"
        )
