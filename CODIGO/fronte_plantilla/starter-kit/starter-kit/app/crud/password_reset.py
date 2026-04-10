from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.models.password_reset import PasswordReset
from app.models.user import User
import secrets
import string


def generate_reset_code(length: int = 6) -> str:
    """Generate a random reset code"""
    characters = string.ascii_uppercase + string.digits
    return ''.join(secrets.choice(characters) for _ in range(length))


def create_password_reset(db: Session, email: str) -> PasswordReset:
    """Create a password reset request"""
    # Delete any existing reset codes for this email
    db.query(PasswordReset).filter(PasswordReset.email == email, PasswordReset.used == 0).delete()

    reset_code = generate_reset_code()
    expires_at = datetime.utcnow() + timedelta(minutes=15)  # 15 minutes expiry

    # Get user if exists
    user = db.query(User).filter(User.email == email).first()
    user_id = user.id if user else None

    password_reset = PasswordReset(
        email=email,
        reset_code=reset_code,
        expires_at=expires_at,
        user_id=user_id
    )

    db.add(password_reset)
    db.commit()
    db.refresh(password_reset)
    return password_reset


def get_password_reset_by_code(db: Session, reset_code: str) -> PasswordReset | None:
    """Get password reset by code"""
    return db.query(PasswordReset).filter(
        PasswordReset.reset_code == reset_code,
        PasswordReset.used == 0,
        PasswordReset.expires_at > datetime.utcnow()
    ).first()


def mark_reset_code_used(db: Session, reset_code: str) -> bool:
    """Mark a reset code as used"""
    reset = db.query(PasswordReset).filter(PasswordReset.reset_code == reset_code).first()
    if reset:
        reset.used = 1
        db.commit()
        return True
    return False


def cleanup_expired_resets(db: Session):
    """Clean up expired password reset codes"""
    db.query(PasswordReset).filter(
        PasswordReset.expires_at < datetime.utcnow()
    ).delete()
    db.commit()