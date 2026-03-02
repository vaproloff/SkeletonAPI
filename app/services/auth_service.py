from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.security import create_access_token, hash_password, verify_password
from app.models.user import User
from app.schemas.user import UserCreate
from app.services.exceptions import AlreadyExistsError


def register_user(db: Session, data: UserCreate) -> User:
    new_user = User(
        email=data.email,
        hashed_password=hash_password(data.password)
    )
    db.add(new_user)

    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        raise AlreadyExistsError("Email already registered") from e

    db.refresh(new_user)
    return new_user


def authenticate_user(db: Session, email: str, password: str) -> User | None:
    user: User = db.query(User).filter(User.email == email).first()
    if user is None:
        return None

    if not verify_password(password, user.hashed_password):
        return None

    return user


def create_token_for_user(user: User) -> str:
    return create_access_token({"email": user.email})
