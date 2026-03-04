from enum import Enum

from sqlalchemy import Column, Integer, String
from sqlalchemy import Enum as SqlEnum
from sqlalchemy.orm import relationship

from app.database import Base


class UserRole(str, Enum):
    ADMIN = "admin"
    USER = "user"

    @property
    def label(self):
        return {
            UserRole.ADMIN: "Admin",
            UserRole.USER: "User"
        }[self]


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(SqlEnum(UserRole,
                          name="user_role",
                          values_callable=lambda enum: [e.value for e in enum]),
                  default=UserRole.USER, server_default="user", nullable=False)
    projects = relationship("Project", back_populates="owner", cascade="all, delete-orphan")
