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
├── api/v1/          # Route handlers — add one file per resource here
├── core/
│   └── config.py    # Settings (pydantic-settings); reads .env; exposes `settings` singleton
├── db/
│   ├── base.py      # DeclarativeBase (`Base`)
│   ├── database.py  # imports settings.DATABASE_URL; exposes DATABASE_URL; no session factory yet
│   └── __init__.py  # exports `Base` and `DATABASE_URL`
├── models/          # SQLAlchemy ORM models; __init__.py re-exports all 6 models
├── services/        # Business logic layer (empty stub)
└── shemas/          # Pydantic schemas — intentional typo, keep it consistent (empty stub)
```

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

`app/core/config.py` defines `Settings(BaseSettings)` with fields: `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASS`. Reads from `.env` at project root. Exposes `settings` singleton and a `DATABASE_URL` property. `app/core/__init__.py` re-exports `settings`.

## Alembic

Initialized. `alembic/env.py` inserts `app/` into `sys.path`, then imports `from db import Base, DATABASE_URL` and `import models` (triggers all model imports for autogenerate). Runs async migrations via `asyncio.run(run_async_migrations())`.

## Key Conventions

- **SQLAlchemy 2.x** with `Mapped`/`mapped_column` typed annotations.
- **Import asymmetry**: ORM models import `Base` from `db` (bare module name, no `app.` prefix) because `app/` is added to `sys.path` at runtime. `alembic/env.py` uses `from app.db import ...` (runs from project root).
- All models must be listed in `app/models/__init__.py` for Alembic autogenerate to detect all tables.

## Missing Dependencies

Not yet in `pyproject.toml`: `PyJWT`, `passlib[bcrypt]`, `pydantic-settings`.

## Infrastructure

`docker-compose.yml` runs PostgreSQL 16 on port **5433** (maps to container 5432). Credentials: `todo_user`/`todo_pass`, DB `todo_db`. Start with `docker compose up -d`.