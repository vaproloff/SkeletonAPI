# FastAPI Backend Skeleton

Production-ready backend skeleton built with FastAPI, PostgreSQL, Alembic, Docker, and JWT authentication.

## Features

- JWT authentication (register, login)
- Projects CRUD with ownership control
- PostgreSQL database
- Alembic migrations
- Pytest test suite
- Docker and docker-compose setup
- Environment-based configuration

---

## Tech Stack

- FastAPI
- SQLAlchemy
- Alembic
- PostgreSQL
- Pytest
- Docker / Docker Compose

---

## Quick Start (Docker)

Clone the repository:

```bash
git clone https://github.com/vaproloff/SkeletonAPI.git
cd SkeletonAPI/
```

Create environment file:

```bash
cp .env.example .env
```

Start services:

```bash
docker compose up --build
```

API will be available at:

```
http://localhost:8000/docs
```

---

## Running Tests

Make sure test database exists:

```bash
docker exec -it skeleton_postgres createdb -U app app_test
```

Run tests:

```bash
pytest -q
```

---

## Database Migrations

Create migration:

```bash
alembic revision --autogenerate -m "message"
```

Apply migration:

```bash
alembic upgrade head
```

---

## Environment Variables

Required variables:

```
DATABASE_URL=postgresql://app:app@db:5432/app_db
JWT_SECRET_KEY=change_me
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

---

## API Overview

### Auth

Register:

```
POST /auth/register
```

Login:

```
POST /auth/token
```

Current user:

```
GET /auth/me
```

---

### Projects

Create project:

```
POST /projects
```

Get projects:

```
GET /projects
```

Get project by id:

```
GET /projects/{id}
```

Delete project:

```
DELETE /projects/{id}
```

---

## Project Structure

```
app/
  api/
  core/
  models/
  schemas/
  main.py

alembic/
tests/
docker-compose.yml
Dockerfile
```

---

## License

MIT