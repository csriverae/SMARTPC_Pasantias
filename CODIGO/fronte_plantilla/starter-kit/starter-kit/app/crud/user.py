from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_user(db: Session, user: UserCreate) -> User:
    # Ensure password is not too long for bcrypt (max 72 bytes)
    password = user.password
    if len(password.encode('utf-8')) > 72:
        password = password[:72]
    
    hashed_password = pwd_context.hash(password)
    db_user = User(email=user.email, password=hashed_password, role=user.role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_users(db: Session) -> list[User]:
    return db.query(User).all()


def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()


def authenticate_user(db: Session, email: str, password: str) -> User | None:
    user = get_user_by_email(db, email)
    if not user:
        return None
    # Truncate password for bcrypt compatibility
    password = password[:72]
    if not pwd_context.verify(password, user.password):
        return None
    return user
