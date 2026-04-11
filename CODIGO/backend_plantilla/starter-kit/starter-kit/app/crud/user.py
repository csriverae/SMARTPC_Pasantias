from sqlalchemy.orm import Session
from app.models.user import User, UserRole
from app.schemas.user import UserCreate
from app.core.security import get_password_hash, verify_password


def create_user(db: Session, user: UserCreate) -> User:
    hashed_password = get_password_hash(user.password)
    role = user.role if user.role else UserRole.employee
    full_name = user.full_name
    if not full_name:
        first = getattr(user, 'first_name', None) or ''
        last = getattr(user, 'last_name', None) or ''
        full_name = f"{first} {last}".strip() or None

    db_user = User(
        email=user.email,
        password=hashed_password,
        full_name=full_name,
        phone=getattr(user, 'phone', None),
        address=getattr(user, 'address', None),
        role=role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_users(db: Session) -> list[User]:
    return db.query(User).all()


def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()


def delete_user(db: Session, user_id: int) -> bool:
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        db.delete(user)
        db.commit()
        return True
    return False


def authenticate_user(db: Session, email: str, password: str) -> User | None:
    user = get_user_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.password):
        return None
    return user


def update_user_password(db: Session, user: User, new_password: str) -> User:
    """Update user password"""
    hashed_password = get_password_hash(new_password)
    user.password = hashed_password
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
