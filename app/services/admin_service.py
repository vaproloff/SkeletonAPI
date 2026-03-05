from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories import user_repo
from app.schemas.user import UserRoleUpdate
from app.services.exceptions import NotFoundError


def set_user_role(db: Session, user_id: int, data: UserRoleUpdate) -> User:
    user: User = user_repo.get_user_by_id(db, user_id)
    if user is None:
        raise NotFoundError("User does not exist")

    user.role = data.role
    db.commit()
    db.refresh(user)

    return user