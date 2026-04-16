"""CRUD operations for DeviceSession"""
from sqlalchemy.orm import Session
from app.models.device_session import DeviceSession
from datetime import datetime, timedelta


def create_device_session(
    db: Session,
    user_id: int,
    device_id: str,
    refresh_token: str,
    device_name: str | None = None,
    device_type: str = "mobile",
    os: str | None = None,
    os_version: str | None = None,
    app_version: str | None = None,
    device_token: str | None = None,
    expires_in_days: int = 30
) -> DeviceSession:
    """Create a new device session"""
    expires_at = datetime.utcnow() + timedelta(days=expires_in_days)
    
    device_session = DeviceSession(
        user_id=user_id,
        device_id=device_id,
        refresh_token=refresh_token,
        device_name=device_name,
        device_type=device_type,
        os=os,
        os_version=os_version,
        app_version=app_version,
        device_token=device_token,
        expires_at=expires_at
    )
    
    db.add(device_session)
    db.commit()
    db.refresh(device_session)
    return device_session


def get_device_session_by_device_id(db: Session, device_id: str) -> DeviceSession | None:
    """Get device session by device ID"""
    return db.query(DeviceSession).filter(DeviceSession.device_id == device_id).first()


def get_device_session_by_id(db: Session, session_id: int) -> DeviceSession | None:
    """Get device session by ID"""
    return db.query(DeviceSession).filter(DeviceSession.id == session_id).first()


def get_user_device_sessions(db: Session, user_id: int, only_active: bool = True) -> list[DeviceSession]:
    """Get all device sessions for a user"""
    query = db.query(DeviceSession).filter(DeviceSession.user_id == user_id)
    
    if only_active:
        query = query.filter(DeviceSession.is_active == True)
    
    return query.all()


def update_device_session_last_accessed(db: Session, device_id: str) -> DeviceSession | None:
    """Update the last accessed timestamp for a device"""
    device_session = get_device_session_by_device_id(db, device_id)
    
    if device_session:
        device_session.last_accessed = datetime.utcnow()
        db.commit()
        db.refresh(device_session)
    
    return device_session


def update_device_token(db: Session, device_id: str, device_token: str) -> DeviceSession | None:
    """Update Firebase/Push notification token for a device"""
    device_session = get_device_session_by_device_id(db, device_id)
    
    if device_session:
        device_session.device_token = device_token
        db.commit()
        db.refresh(device_session)
    
    return device_session


def deactivate_device_session(db: Session, device_id: str) -> bool:
    """Deactivate a specific device session (logout from device)"""
    device_session = get_device_session_by_device_id(db, device_id)
    
    if device_session:
        device_session.is_active = False
        db.commit()
        return True
    
    return False


def deactivate_all_user_devices(db: Session, user_id: int) -> int:
    """Deactivate all device sessions for a user (logout from all devices)"""
    devices = db.query(DeviceSession).filter(DeviceSession.user_id == user_id).all()
    
    for device in devices:
        device.is_active = False
    
    db.commit()
    return len(devices)


def delete_device_session(db: Session, device_id: str) -> bool:
    """Delete a device session"""
    device_session = get_device_session_by_device_id(db, device_id)
    
    if device_session:
        db.delete(device_session)
        db.commit()
        return True
    
    return False


def cleanup_expired_sessions(db: Session) -> int:
    """Remove expired device sessions"""
    expired = db.query(DeviceSession).filter(DeviceSession.expires_at <= datetime.utcnow()).all()
    
    for session in expired:
        db.delete(session)
    
    db.commit()
    return len(expired)
