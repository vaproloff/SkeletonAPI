from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from app.api import all_routers
from app.services.exceptions import AlreadyExistsError, NotFoundError

app = FastAPI()


@app.exception_handler(NotFoundError)
def not_found_handler(request: Request, exc: NotFoundError):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": str(exc)}
    )


@app.exception_handler(AlreadyExistsError)
def already_exists_handler(request: Request, exc: AlreadyExistsError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": str(exc)}
    )


for r in all_routers:
    app.include_router(r)
