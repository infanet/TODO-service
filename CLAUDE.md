# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

A FastAPI TODO service with JWT authentication and PostgreSQL, managed with **Poetry**.

## Commands

```bash
poetry install                          # Install dependencies
uvicorn app.main:app --reload           # Run dev server (from project root)
black .                                 # Format code
```

## Architecture

The app lives entirely under `app/`, with the entry point at `app/main.py`. The module layout follows:

```
app/
├── main.py          # FastAPI app instance and router registration
├── api/v1/          # Route handlers (currently empty, add per-resource files here)
├── core/            # Settings, JWT, password hashing utilities
├── db/              # SQLAlchemy Base (DeclarativeBase) and session factory
├── models/          # SQLAlchemy ORM models (users.py exists)
├── services/        # Business logic layer
└── shemas/          # Pydantic schemas (note: directory name is "shemas", not "schemas")
```

## Key Conventions

- **SQLAlchemy 2.x** with `Mapped`/`mapped_column` typed annotations; `Base` is imported from `app.db`
- Models import `Base` from `db` (not `app.db`) — the app is run from the project root with `app.main:app`, so `app/` is on sys.path
- `docker-compose.yml` exists at the root for spinning up PostgreSQL (currently empty — populate as needed)
- The `shemas/` directory name is a known typo; keep it consistent when adding new schema files