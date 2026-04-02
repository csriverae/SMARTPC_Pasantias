from pydantic import BaseModel
from typing import Any, Dict, List, Optional


class ResponseData(BaseModel):
    """Estructura de datos para la respuesta"""
    data: List[Any] = []


class StandardResponse(BaseModel):
    """Formato estándar de respuesta"""
    message: str
    status: int
    error: bool
    data: ResponseData = ResponseData()


class SuccessResponse(StandardResponse):
    """Respuesta exitosa"""
    def __init__(self, message: str, data: Any = None, status: int = 200, **kwargs):
        if data is None:
            data = ResponseData()
        elif isinstance(data, list):
            data = ResponseData(data=data)
        elif isinstance(data, dict) and "data" in data:
            data = ResponseData(**data)
        else:
            data = ResponseData(data=[data] if not isinstance(data, list) else data)
        
        super().__init__(
            message=message,
            status=status,
            error=False,
            data=data,
            **kwargs
        )


class ErrorResponse(StandardResponse):
    """Respuesta de error"""
    def __init__(self, message: str, error_detail: str = None, status: int = 400, **kwargs):
        error_info = {}
        if error_detail:
            error_info["error"] = error_detail
        
        super().__init__(
            message=message,
            status=status,
            error=True,
            data=ResponseData(data=[error_info] if error_info else []),
            **kwargs
        )
