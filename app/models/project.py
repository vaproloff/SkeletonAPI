from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, UniqueConstraint, func
from sqlalchemy.orm import relationship

from app.database import Base


class Project(Base):
    __tablename__ = "project"
    __table_args__ = (UniqueConstraint("name", "owner_id", name="uq_project_owner_name"),)

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    owner_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    owner = relationship("User", back_populates="projects")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )
