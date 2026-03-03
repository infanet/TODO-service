# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

A FastAPI TODO service with JWT authentication and PostgreSQL, managed with **Poetry**.

## Commands

```bash
poetry install                              # Install dependencies
uvicorn app.main:app --reload               # Run dev server (from project root)
black .                                     # Format code
alembic upgrade head                        # Apply migrations
alembic revision --autogenerate -m "msg"    # Generate a migration
alembic init alembic                        # First-time Alembic setup (not yet done)
```

## Architecture

The app lives entirely under `app/`, entry point at `app/main.py`.

```
app/
├── main.py          # FastAPI app instance and router registration
├── api/v1/          # Route handlers — add one file per resource here
├── core/            # Settings, JWT, password hashing utilities (empty)
├── db/
│   └── base.py      # DeclarativeBase (`Base`) — session factory not yet added
├── models/          # SQLAlchemy ORM models
├── services/        # Business logic layer (empty)
└── shemas/          # Pydantic schemas — intentional typo, keep it consistent
```

## Data Model

Five ORM models, all inheriting `Base` from `db` (not `app.db`):

- **`User`** — `email` (unique, indexed), `hashed_password`, `created_at`; owns `Todo` list, `Tag` list, and one `RefreshToken`
- **`Todo`** — FK→`users.id`, `title`, `description` (TEXT), `is_completed` (bool), `priority` (`Priority` enum: low/medium/high), `created_at`, `updated_at`
- **`Tag`** — FK→`users.id`, `name` (unique); per-user labels
- **`TodoTags`** — join table (`todo_id`, `tag_id`) with composite PK; links todos↔tags
- **`RefreshToken`** — FK→`users.id`, `token` (TEXT, unique), `expires_at`, `is_revoked`, `created_at`

## Key Conventions

- **SQLAlchemy 2.x** with `Mapped`/`mapped_column` typed annotations.
- Models import `Base` from `db` (bare, not `app.db`) — `app/` is on `sys.path` via the `app.main:app` entry point.
- `docker-compose.yml` is at the root but currently empty — needs PostgreSQL service.
- Alembic is installed but **not yet initialized**. When initializing, configure `env.py` to import all models so autogenerate can detect them.
- `app/core/`, `app/services/`, `app/shemas/` are empty stubs — next areas to build out.
- Missing dependencies not yet in `pyproject.toml`: `asyncpg`, `PyJWT`, `passlib[bcrypt]`, `pydantic-settings`.