from sqlalchemy.orm import Session
from app.models.user import User, UserRole
from app.schemas.user import UserCreate
from app.core.security import get_password_hash, verify_password


def create_user(db: Session, user: UserCreate | dict) -> User:
    # Hash password using bcrypt directly (imported in security.py)
    if isinstance(user, dict):
        # Handle dict input (from service layer)
        if 'password' in user and not user['password'].startswith('$2b$'):
            user['password'] = get_password_hash(user['password'])
        db_user = User(**user)
    else:
        # Handle UserCreate schema input
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
            role=role
        )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user(db: Session, user_id: int) -> User | None:
    """Get user by ID"""
    return db.query(User).filter(User.id == user_id).first()


def get_users(db: Session) -> list[User]:
    return db.query(User).all()


def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()


def update_user(db: Session, user_id: int, update_data: dict) -> User | None:
    """Update user with provided data"""
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        for key, value in update_data.items():
            if hasattr(user, key) and value is not None:
                setattr(user, key, value)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    return None


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
