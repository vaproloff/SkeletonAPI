from factories import auth_headers, create_user

from app.models.user import UserRole


def test_get_admins_project_page_from_user(client, db_session):
    user = create_user(db_session, email="user@test.com", password="secret")
    headers = auth_headers(client, email=user.email, password="secret")

    r = client.get("/admin/projects", headers=headers)
    assert r.status_code == 403, r.text
    assert r.json()["detail"] == "Not enough permissions"


def test_get_admins_project_page_from_admin(client, db_session):
    user1 = create_user(db_session, email="user1@test.com", password="secret")
    u1_headers = auth_headers(client, email=user1.email, password="secret")
    p1 = client.post("/projects", json={"name": "project 1"}, headers=u1_headers)
    assert p1.status_code == 200, p1.text

    user2 = create_user(db_session, email="user2@test.com", password="secret")
    u2_headers = auth_headers(client, email=user2.email, password="secret")
    p2 = client.post("/projects", json={"name": "project 2"}, headers=u2_headers)
    assert p2.status_code == 200, p2.text

    admin = create_user(db_session, email="admin@test.com", password="secret", role=UserRole.ADMIN)
    a_headers = auth_headers(client, email=admin.email, password="secret")

    r = client.get("/admin/projects", headers=a_headers)
    assert r.status_code == 200, r.text
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2


def test_admin_tries_set_role(client, db_session):
    admin = create_user(db_session, email="admin@test.com", password="secret", role=UserRole.ADMIN)
    a_headers = auth_headers(client, email=admin.email, password="secret")

    user = create_user(db_session, email="user@test.com", password="secret")
    u_headers = auth_headers(client, email=user.email, password="secret")

    r_a = client.patch(f"/admin/users/{user.id}/role", json={"role": "admin"}, headers=a_headers)
    assert r_a.status_code == 200, r_a.text
    assert r_a.json()["role"] == "admin"

    r_u = client.get("/admin/projects", headers=u_headers)
    assert r_u.status_code == 200, r_u.text


def test_user_tries_set_role(client, db_session):
    user1 = create_user(db_session, email="user1@test.com", password="secret")
    u1_headers = auth_headers(client, email=user1.email, password="secret")

    create_user(db_session, email="user2@test.com", password="secret")

    r = client.patch("/admin/users/2/role", json={"role": "admin"}, headers=u1_headers)
    assert r.status_code == 403, r.text
    assert r.json()["detail"] == "Not enough permissions"
