from app.api.auth import router as auth_router
from app.api.health import router as health_router
from app.api.projects import router as projects_router

all_routers = [health_router, auth_router, projects_router]
