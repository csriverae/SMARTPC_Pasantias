from typing import Any, Dict
from pydantic import BaseModel
from fastapi import status


class StandardResponse(BaseModel):
    message: str
    status: int
    error: bool
    data: Any


def success_response(message: str, data: Any = None, status_code: int = status.HTTP_200_OK) -> Dict[str, Any]:
    if data is None:
        data = {}
    return {
        "message": message,
        "status": status_code,
        "error": False,
        "data": data,
    }


def not_found_response(message: str = "Not Found", detail: Any = None) -> Dict[str, Any]:
    return {
        "message": message,
        "status": status.HTTP_404_NOT_FOUND,
        "error": True,
        "data": {"error": detail or message},
    }


def internal_error_response(message: str = "Internal Server Error", technical: str | None = None) -> Dict[str, Any]:
    return {
        "message": message,
        "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
        "error": True,
        "data": {"error": technical or message},
    }
