from pydantic import BaseModel, ConfigDict, EmailStr

from app.models.user import UserRole


class UserCreate(BaseModel):
    email: str
    password: str


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: EmailStr
    role: UserRole
