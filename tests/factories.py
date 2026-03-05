from app.core.security import hash_password
from app.models.user import User, UserRole


def create_user(
        db_session,
        email: str,
        password: str = "secret",
        role: UserRole = UserRole.USER
) -> User:
    user = User(email=email, hashed_password=hash_password(password), role=role)
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    return user


def auth_headers(client, email: str, password: str):
    t = client.post("/auth/token", data={"username": email, "password": password})
    assert t.status_code == 200, t.text

    token = t.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
