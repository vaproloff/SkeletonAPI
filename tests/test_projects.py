import time


def _auth_headers(client, email: str, password: str):
    client.post("auth/register", json={"email": email, "password": password})
    t = client.post("auth/token", data={"username": email, "password": password})
    token = t.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_project_ownership_404_for_other_user(client):
    h1 = _auth_headers(client, email="u1@test.com", password="secret")
    h2 = _auth_headers(client, email="u2@test.com", password="secret")

    p = client.post("/projects", json={"name": "u1 project"}, headers=h1)
    assert p.status_code == 200, p.text
    project_id = p.json()["id"]

    r = client.get(f'/projects/{project_id}', headers=h2)
    assert r.status_code == 404, r.text

    r2 = client.get(f'/projects/{project_id}', headers=h1)
    assert r2.status_code == 200, r2.text
    data = r2.json()
    assert data["name"] == "u1 project"
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data


def test_updated_at_changes_on_patch(client):
    headers = _auth_headers(client, email="t@test.com", password="secret")

    p = client.post("/projects", json={"name": "v1"}, headers=headers)
    assert p.status_code == 200, p.text
    project = p.json()
    project_id = project["id"]
    updated_before = project["updated_at"]

    time.sleep(0.01)

    r = client.patch(f"/projects/{project_id}", json={"name": "v2"}, headers=headers)
    assert r.status_code == 200, r.text
    updated_after = r.json()["updated_at"]

    assert updated_after != updated_before


def test_delete_project_removes_it(client):
    headers = _auth_headers(client, email="del@test.com", password="secret")

    p = client.post("/projects", json={"name": "to_delete"}, headers=headers)
    assert p.status_code == 200, p.text
    project_id = p.json()["id"]

    d = client.delete(f"/projects/{project_id}", headers=headers)
    assert d.status_code == 204, d.text

    r = client.get(f'/projects/{project_id}', headers=headers)
    assert r.status_code == 404, r.text
