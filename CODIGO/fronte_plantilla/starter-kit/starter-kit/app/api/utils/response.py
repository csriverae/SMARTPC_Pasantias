from typing import Any, Dict, Optional
from pydantic import BaseModel
from fastapi import status


class StandardResponse(BaseModel):
    """Standard API response format"""
    message: str
    status: int
    error: bool
    data: Any = None


def success_response(
    message: str = "Success",
    data: Any = None,
    status_code: int = status.HTTP_200_OK
) -> Dict[str, Any]:
    """Format successful response"""
    return {
        "message": message,
        "status": status_code,
        "error": False,
        "data": data if data is not None else {},
    }


def error_response(
    message: str,
    status_code: int = status.HTTP_400_BAD_REQUEST,
    error_code: Optional[str] = None,
    details: Optional[Any] = None
) -> Dict[str, Any]:
    """Format error response"""
    data = {}
    if error_code:
        data["error_code"] = error_code
    if details:
        data["details"] = details
    
    return {
        "message": message,
        "status": status_code,
        "error": True,
        "data": data if data else None,
    }


def not_found_response(
    message: str = "Not Found",
    resource: Optional[str] = None,
    detail: Any = None
) -> Dict[str, Any]:
    """Format not found error"""
    if resource and not message.startswith(resource):
        message = f"{resource} not found"
    
    return error_response(
        message=message,
        status_code=status.HTTP_404_NOT_FOUND,
        details=detail
    )


def internal_error_response(
    message: str = "Internal Server Error",
    technical: Optional[str] = None
) -> Dict[str, Any]:
    """Format internal server error"""
    return error_response(
        message=message,
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        details=technical
    )


def unauthorized_response(
    message: str = "Unauthorized",
    detail: Optional[str] = None,
    error_code: str = "AUTH_ERROR"
) -> Dict[str, Any]:
    """Format unauthorized error"""
    return error_response(
        message=message,
        status_code=status.HTTP_401_UNAUTHORIZED,
        error_code=error_code,
        details=detail
    )


def forbidden_response(
    message: str = "Forbidden",
    detail: Optional[str] = None
) -> Dict[str, Any]:
    """Format forbidden error"""
    return error_response(
        message=message,
        status_code=status.HTTP_403_FORBIDDEN,
        details=detail
    )


def conflict_response(
    message: str,
    detail: Optional[str] = None,
    field: Optional[str] = None
) -> Dict[str, Any]:
    """Format conflict error (e.g., duplicate email)"""
    data = {"error": detail or message}
    if field:
        data["field"] = field
    
    return {
        "message": message,
        "status": status.HTTP_409_CONFLICT,
        "error": True,
        "data": data
    }


def validation_error_response(
    message: str = "Validation error",
    field: Optional[str] = None,
    details: Optional[Any] = None
) -> Dict[str, Any]:
    """Format validation error"""
    data = {"error": message}
    if field:
        data["field"] = field
    if details:
        data["details"] = details
    
    return {
        "message": message,
        "status": status.HTTP_400_BAD_REQUEST,
        "error": True,
        "data": data
    }


def created_response(
    message: str = "Created",
    data: Any = None
) -> Dict[str, Any]:
    """Format 201 Created response"""
    return success_response(
        message=message,
        data=data,
        status_code=status.HTTP_201_CREATED
    )


def no_content_response() -> Dict[str, Any]:
    """Format 204 No Content response"""
    return {
        "message": "No content",
        "status": status.HTTP_204_NO_CONTENT,
        "error": False,
        "data": None,
    }
