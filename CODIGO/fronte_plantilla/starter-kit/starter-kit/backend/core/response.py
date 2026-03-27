from typing import Any


def api_success(message: str, data: Any, status: int = 200):
    return {
        "message": message,
        "status": status,
        "error": False,
        "data": data,
    }


def api_error(message: str, status: int = 400, error_data: Any = None):
    payload = {"data": []}
    if error_data is not None:
        payload["error"] = str(error_data)
    return {
        "message": message,
        "status": status,
        "error": True,
        "data": payload,
    }
