"""Pydantic schemas for device sessions"""
from pydantic import BaseModel
from datetime import datetime


class DeviceInfo(BaseModel):
    """Device information for registration"""
    device_id: str  # Unique device identifier
    device_name: str | None = None  # e.g., "iPhone 12 Pro", "Samsung Galaxy S21"
    device_type: str = "mobile"  # mobile, tablet, web
    os: str | None = None  # iOS, Android, Windows, etc.
    os_version: str | None = None
    app_version: str | None = None
    device_token: str | None = None  # Firebase/Push notification token


class DeviceSessionRequest(BaseModel):
    """Request to register or validate a device session"""
    device_id: str
    device_info: DeviceInfo


class DeviceSessionResponse(BaseModel):
    """Response for device session operations"""
    device_id: str
    device_name: str | None
    device_type: str
    os: str | None
    last_accessed: datetime
    created_at: datetime


class UserDevicesResponse(BaseModel):
    """Response containing list of user devices"""
    devices: list[DeviceSessionResponse]
    total: int


class MobileLoginRequest(BaseModel):
    """Enhanced login request for mobile devices"""
    email: str
    password: str
    device_info: DeviceInfo
    remember_device: bool = True  # Whether to create persistent session


class MobileLoginResponse(BaseModel):
    """Response for mobile login with device session"""
    access_token: str
    refresh_token: str
    token_type: str
    tenant_id: str
    device_id: str
    user: dict


class DeviceValidationResponse(BaseModel):
    """Response for device validation"""
    is_valid: bool
    device_id: str | None = None
    email: str | None = None
    tenant_id: str | None = None
    access_token: str | None = None
    message: str | None = None
