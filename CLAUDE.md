# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

A FastAPI TODO service with JWT authentication and PostgreSQL, managed with **Poetry**.

## Commands

```bash
poetry install                          # Install dependencies
uvicorn app.main:app --reload           # Run dev server (from project root)
black .                                 # Format code
alembic upgrade head                    # Apply migrations (once Alembic is configured)
alembic revision --autogenerate -m "msg"  # Generate a migration
```

## Architecture

The app lives entirely under `app/`, with the entry point at `app/main.py`.

```
app/
├── main.py          # FastAPI app instance and router registration
├── api/v1/          # Route handlers — add one file per resource here
├── core/            # Settings, JWT, password hashing utilities (currently empty)
├── db/              # DeclarativeBase (`Base`) and session factory (session factory not yet added)
├── models/          # SQLAlchemy ORM models: users.py, todos.py
├── services/        # Business logic layer (currently empty)
└── shemas/          # Pydantic schemas — note the intentional typo, keep it consistent
```

## Key Conventions

- **SQLAlchemy 2.x** with `Mapped`/`mapped_column` typed annotations.
- Models import `Base` from `db` (bare, not `app.db`) — the app is run from the project root, so `app/` is on `sys.path` via the `app.main:app` entry point.
- `Todos` has a FK to `users.id`; `User` has `email` (unique, indexed), `hashed_password`, and `created_at`.
- `docker-compose.yml` exists at the root but is currently empty — populate it to spin up PostgreSQL.
- Alembic is installed but not yet initialized; run `alembic init alembic` from the project root when ready, then configure `env.py` to import all models before running migrations.