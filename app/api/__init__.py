from app.api.auth import router as auth_router
from app.api.health import router as health_router

all_routers = [health_router, auth_router]
