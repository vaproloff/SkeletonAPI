from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.auth import require_role
from app.database import get_db
from app.models.user import User, UserRole
from app.schemas.project import ProjectsPageOut
from app.services import project_service

router = APIRouter(prefix="/admin", tags=["admin"])

@router.get("/projects", response_model=ProjectsPageOut)
def get_projects(
        limit: int = Query(default=20, ge=1, le=100),
        offset: int = Query(default=0, ge=0),
        _admin: User = Depends(require_role(UserRole.ADMIN)),
        db: Session = Depends(get_db),
):
    return project_service.get_projects_page_admin(db, limit=limit, offset=offset)