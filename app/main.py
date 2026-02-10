from fastapi import FastAPI

from app.models import user
from app.database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/health")
def health():
    return {"status": "ok"}
