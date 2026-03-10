# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

A FastAPI TODO service with JWT authentication, managed with **Poetry**. Uses PostgreSQL via `asyncpg`. Configuration is read from a `.env` file via `pydantic-settings`.

## Commands

```bash
poetry install                              # Install dependencies
uvicorn app.main:app --reload               # Run dev server (from project root)
black .                                     # Format code
alembic upgrade head                        # Apply migrations (from project root)
alembic revision --autogenerate -m "msg"    # Generate a migration (from project root)
```

## Architecture

The app lives under `app/`, entry point at `app/main.py`.

```
app/
├── main.py          # FastAPI app instance and router registration
├── api/v1/
│   ├── router.py    # Top-level v1 router (prefix /api/v1); includes resource routers
│   ├── __init__.py  # re-exports resource routers for router.py
│   └── users/       # One directory per resource
│       ├── router_users.py   # Assembles all user CRUD routers
│       ├── get_users.py      # GET /users
│       ├── get_user.py       # GET /users/{id}
│       ├── post_user.py      # POST /users
│       ├── put_user.py       # PUT /users/{id}
│       └── delete_user.py    # DELETE /users/{id}
├── core/
│   └── config.py    # Settings (pydantic-settings); reads .env; exposes `settings` singleton
├── db/
│   ├── base.py      # DeclarativeBase (`Base`)
│   ├── database.py  # exposes DATABASE_URL, async_engine, async_session_factory, get_async_session
│   └── __init__.py  # exports `Base`, `DATABASE_URL`, `get_async_session`
├── models/          # SQLAlchemy ORM models; __init__.py re-exports all 6 models
├── schemas/         # Pydantic schemas; one subdirectory per resource (e.g. schemas/users/)
│   └── users/       # UserBase, UserCreate, UserResponse
├── services/        # Business logic layer; thin functions that accept a repository and call it
├── repositories/    # Data access layer; classes (e.g. UserRepository) that wrap AsyncSession queries
└── shemas/          # (legacy empty stub — use schemas/ for all new schemas)
```

### Routing Pattern

Each resource lives in its own directory under `app/api/v1/`. CRUD operations are split into separate files, each exposing a `router`. A `router_<resource>.py` file assembles them with `include_router`. Then `app/api/v1/router.py` includes each resource router under the `/api/v1` prefix, and `app/main.py` registers that top-level router.

### Layered Architecture

Requests flow: **router → service → repository**.

- **Repository** (e.g. `UserRepository`) wraps `AsyncSession` and exposes named query methods (`all_users`, etc.). Instantiated in the route handler with the injected session.
- **Service** (e.g. `get_users`) is a plain async function that receives a repository instance and contains business logic.
- **Router** creates the repository, calls the service, and returns a response.

## Data Model

Six ORM models (all inherit `Base` from `app.db`). `TodoTags` is a join table, not exported from `__init__.py`.

- **`User`** — `username`, `email` (unique, indexed), `hashed_password`, `is_active`, `created_at`; owns `todo`, `tag`, `refresh_token`, `category`, `comment` relationships
- **`Todo`** — FK→`users.id`, FK→`categories.id`; `title`, `description` (TEXT), `status` (`Status` enum: todo/done/in_progress), `priority` (`Priority` enum: low/medium/high), `deadline`, `created_at`, `updated_at`
- **`Tag`** — FK→`users.id`, `name`, `color` (String(7), default `#10b981`); unique per user via `UniqueConstraint("user_id", "name")`
- **`TodoTags`** — join table (`todo_id`, `tag_id`) with composite PK; `Todo`↔`Tag` many-to-many via `secondary="todo_tags"` (viewonly) + explicit `items` relationships for writes
- **`RefreshToken`** — FK→`users.id`, `token` (TEXT, unique), `expires_at`, `is_revoked`, `created_at`
- **`Category`** — FK→`users.id`, `name`, `color` (String(7)), `created_at`; owns relationship to `Todo`
- **`Comment`** — FK→`users.id`, FK→`todos.id`, `content` (TEXT), `created_at`

## Configuration

`app/core/config.py` defines `Settings(BaseSettings)` with fields: `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASS`. Reads from `.env` at project root. Exposes `settings` singleton and a `DATABASE_URL` property (returns `postgresql+asyncpg://...` URL). `app/core/__init__.py` re-exports `settings`.

## Alembic

Initialized. `alembic/env.py` inserts `app/` into `sys.path`, then imports `from db import Base, DATABASE_URL` and `import models` (triggers all model imports for autogenerate). Sets `sqlalchemy.url` from `DATABASE_URL` at runtime, so `alembic.ini` URL is ignored. Runs async migrations via `asyncio.run(run_async_migrations())`.

## Key Conventions

- **SQLAlchemy 2.x** with `Mapped`/`mapped_column` typed annotations.
- **Import asymmetry**: Route handlers and ORM models import from bare module names (`from db import ...`, `from models import ...`) because `app/` is on `sys.path` at runtime. `alembic/env.py` uses `from app.db import ...` (runs from project root where `app/` is not on `sys.path`).
- All models must be listed in `app/models/__init__.py` for Alembic autogenerate to detect all tables.
- **Session DI**: inject `AsyncSession` via `Depends(get_async_session)` (imported from `db`).

## Missing Dependencies

Not yet in `pyproject.toml` (verify before using): `PyJWT`, `passlib[bcrypt]`, `pydantic-settings`.

## Infrastructure

`docker-compose.yml` runs PostgreSQL 16 on port **5433** (maps to container 5432). Credentials: `todo_user`/`todo_pass`, DB `todo_db`. Start with `docker compose up -d`.