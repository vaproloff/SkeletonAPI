from fastapi import FastAPI

from app.api import all_routers
from app.database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

for r in all_routers:
    app.include_router(r)
