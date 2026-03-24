# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

A FastAPI TODO service, managed with **Poetry**. Uses PostgreSQL via `asyncpg`. Configuration is read from a `.env` file via `pydantic-settings` (bundled inside `fastapi[all]`).

Password hashing and JWT authentication are implemented in `app/core/security.py`. Access + refresh tokens use symmetric HS256 signing. The `RefreshToken` model persists refresh tokens in the DB. Protected routes use the `get_current_user` dependency from `app/api/v1/dependencies.py`.

## Commands

```bash
poetry install                              # Install dependencies
uvicorn app.main:app --reload               # Run dev server (from project root)
ruff format .                               # Format code
ruff check .                                # Lint
ruff check --fix .                          # Auto-fix lint issues
alembic upgrade head                        # Apply migrations (from project root)
alembic revision --autogenerate -m "msg"    # Generate a migration (from project root)
docker compose up -d                        # Start PostgreSQL container
```

## Architecture

The app lives under `app/`, entry point at `app/main.py`. `app/main.py` inserts `app/` into `sys.path` so all internal imports use bare module names (no `app.` prefix).

```
app/
├── main.py          # FastAPI app instance and router registration; adds app/ to sys.path
├── api/
│   ├── __init__.py  # exports v1_router
│   └── v1/
│       ├── router.py          # Top-level v1 router (prefix /api/v1); includes resource routers
│       ├── auth/              # POST /register, POST /login, POST /refresh, POST /logout
│       ├── users/             # GET /all, GET /one, POST /create, DELETE /delete
│       ├── categories/        # GET /, GET /one, POST /create, PATCH /patch, DELETE /delete
│       ├── todos/             # GET /all, GET /one, POST /create, PATCH /patch, DELETE /delete
│       ├── tags/              # GET /all, GET /one, POST /create, PATCH /patch, DELETE /delete
│       ├── comments/          # GET /all, GET /item, POST /create, PUT /update, DELETE /delete
│       └── dependencies.py    # get_current_user — FastAPI dependency for protected routes
├── core/
│   ├── config.py          # Settings (pydantic-settings); reads .env; exposes `settings` singleton
│   ├── exceptions.py      # AllError class — returns HTTPException via .not_found() / .bad_request()
│   ├── error_messages.py  # ErrorMessages class — string constants (USER_404, CATEGORY_404, etc.)
│   ├── security.py        # hash_password, verify_password (bcrypt), create_access_token, create_refresh_token, decode_token
│   └── logging.py         # setup_logging (call once at startup), get_logger(name) — stdlib logging to stdout
├── db/
│   ├── base.py      # DeclarativeBase (`Base`)
│   ├── database.py  # exposes DATABASE_URL, async_engine, async_session_factory, get_async_session
│   └── __init__.py  # exports `Base`, `DATABASE_URL`, `get_async_session`
├── models/          # SQLAlchemy ORM models; __init__.py re-exports all (except TodoTags)
├── schemas/         # Pydantic schemas; __init__.py re-exports all (see below)
│   ├── users/       # exported: UserCreate, UserResponse
│   ├── categories/  # exported: CategoryCreate, CategoryResponse, CategoryPatch, CategoriesUserResponse
│   ├── todos/       # exported: TodoCreate, TodoResponse, TodoPatch, TodoItems
│   │                # internal: TodosCategory (defined in todo_response.py, used for nesting)
│   ├── tags/        # exported: TagCreate, TagPatch, TagResponse, TagItem
│   ├── comments/    # exported: CommentCreate, CommentResponse, CommentItemResponse
│   │                # internal: TodoComment (defined in comment_response.py, used for nesting)
│   └── auth/        # exported: TokenResponse, RefreshRequest
├── services/        # Business logic as classes; __init__.py re-exports UserService, CategoryService, TodoService, TagService, CommentService, AuthService
└── repositories/    # Data access as classes; __init__.py re-exports UserRepository, CategoryRepository, TodoRepositories, TagRepositories, CommentRepositories, RefreshTokenRepository
```

### Routing Pattern

Each resource lives in its own directory under `app/api/v1/`. CRUD operations are split into separate files, each exposing a `router`. A `router_<resource>.py` assembles them with `include_router`. Then `app/api/v1/router.py` includes each resource router under the `/api/v1` prefix.

### Layered Architecture

Requests flow: **router → service → repository**.

- **Repository** wraps `AsyncSession` and exposes named query methods. Always calls `commit()` + `refresh()` after writes (refresh is needed to get server-generated fields: `id`, `created_at`, etc.).
- **Service** takes `session: AsyncSession` in `__init__`. Each service owns a `get_404_not_found(id)` method that fetches the resource and raises a 404 if missing. Services that validate foreign entities inject the relevant service (not repository) — e.g. `CategoryService` holds a `UserService` instance and calls `self.user_services.get_404_not_found(user_id)`.
- **Router** instantiates the service with the injected session and calls its method.

### Service Dependency Pattern

Services compose other services for cross-entity validation:

```python
class CategoryService:
    def __init__(self, session: AsyncSession):
        self.user_services = UserService(session)        # delegates user validation
        self.category_repositories = CategoryRepository(session)

    async def get_404_not_found(self, category_id: int):
        category = await self.category_repositories.get_by_id(category_id)
        if not category:
            raise AllError(ErrorMessages.CATEGORY_404).not_found()
        return category

    async def create_category(self, user: User, category: CategoryCreate):
        await self.user_services.get_404_not_found(user.id)  # validate user exists
        return await self.category_repositories.create(category=category, user_id=user.id)
```

Dependency chains: `CommentService` → `TodoService` → `CategoryService` → `UserService`, and `TagService` → `TodoService` → `CategoryService` → `UserService`.

### Error Handling Pattern

```python
from core import AllError, ErrorMessages

raise AllError(ErrorMessages.USER_404).not_found()      # 404
raise AllError(ErrorMessages.USER_400).bad_request()    # 400
raise AllError("Token expired").unauthorized()           # 401 (with WWW-Authenticate: Bearer)
raise AllError(ErrorMessages.FORBIDDEN_403).forbidden() # 403
```

`ErrorMessages` holds string constants. `AllError(detail)` wraps them into `HTTPException`.

### Authorization Pattern

All write/read-one operations check that the resource belongs to the authenticated user. `UserService.check_current` is a static method used for this:

```python
# In any service method, after fetching the resource:
await self.user_services.check_current(
    data_id=resource.user_id,   # owner stored on the resource
    current_user_id=user.id,    # current_user injected by get_current_user
)
```

Protected routes inject `current_user: User = Depends(get_current_user)` (imported from `..dependencies`) and pass it down to the service. The service never queries the user from the DB again — it uses the `User` object directly.

### Patch Pattern (repositories)

```python
update_data = new_data.model_dump(exclude_unset=True)  # only fields sent by client
for key, value in update_data.items():
    setattr(obj, key, value)
await self.session.commit()
await self.session.refresh(obj)
```

### Put Pattern (full update, repositories)

```python
for key, value in new_data.model_dump().items():  # all fields, no exclude_unset
    setattr(obj, key, value)
await self.session.commit()
await self.session.refresh(obj)
```

Use `model_dump()` without `exclude_unset=True` — updates all fields regardless of what was sent.

### Delete Pattern

Repository only deletes — no refresh (object is gone):
```python
await self.session.delete(obj)
await self.session.commit()
```

Service fetches the object first (to return it), then deletes:
```python
obj = await self.repo.get_by_id(obj_id)
if not obj:
    raise AllError(ErrorMessages.X_404).not_found()
await self.repo.del_x(obj)
return obj  # returns the deleted object
```

DELETE endpoints return the deleted object as their response model.

### Nested Query Pattern (repositories)

For fetching a nested hierarchy (e.g. user → category → todo), repositories use `selectinload` with `with_loader_criteria` to filter related collections in a single query:

```python
result = await self.session.execute(
    select(User)
    .options(
        selectinload(User.categories).selectinload(Category.todos),
        with_loader_criteria(Category, Category.id == category_id),
        with_loader_criteria(Todo, Todo.id == todo_id),
    )
    .where(User.id == user_id)
)
return result.scalar_one_or_none()
```

The response schema mirrors this nesting: `TodoItems(UserResponse)` contains `categories: list[TodosCategory]`, and `TodosCategory(CategoryResponse)` contains `todos: list[TodoResponse]`.

### Pydantic Schemas

`model_config = ConfigDict(from_attributes=True)` is required **only in Response schemas** — they receive SQLAlchemy objects from the DB. Create/Patch schemas receive plain JSON and do not need it.

Response schemas that nest other resource types import from the top-level `schemas` package (e.g. `from schemas import UserResponse`), not from sibling modules. This is the correct pattern to avoid circular imports between subpackages.

## API Routes

All routes are under `/api/v1`.

### Auth (`/auth`)
| Method | Path | Auth required | Body |
|--------|------|--------------|------|
| POST | `/register` | No | `UserCreate` |
| POST | `/login` | No | `OAuth2PasswordRequestForm` (form data) |
| POST | `/refresh` | Yes | `RefreshRequest` |
| POST | `/logout` | Yes | `RefreshRequest`; returns 204 No Content |

Login returns `TokenResponse` with `access_token` and `refresh_token`. Protected routes use `OAuth2PasswordBearer` pointing to `/api/v1/auth/login`.

### Users (`/users`)
| Method | Path | Query params | Body |
|--------|------|-------------|------|
| GET | `/all` | — | — |
| GET | `/one` | `user_id` | — |
| POST | `/create` | — | `UserCreate` |
| DELETE | `/delete` | `user_id` | — |

### Categories (`/categories`)
| Method | Path | Query params | Body |
|--------|------|-------------|------|
| GET | `/` | — | — |
| GET | `/one` | `category_id` | — |
| POST | `/create` | — | `CategoryCreate` |
| PATCH | `/patch` | `category_id` | `CategoryPatch` |
| DELETE | `/delete` | `category_id` | — |

### Todos (`/todos`)
| Method | Path | Query params | Body |
|--------|------|-------------|------|
| GET | `/all` | `category_id` | — |
| GET | `/one` | `category_id`, `todo_id` | — |
| POST | `/create` | `category_id` | `TodoCreate` |
| PATCH | `/patch` | `category_id`, `todo_id` | `TodoPatch` |
| DELETE | `/delete` | `todo_id` | — |

### Tags (`/tags`)
| Method | Path | Query params | Body |
|--------|------|-------------|------|
| GET | `/all` | `todo_id` | — |
| GET | `/one` | `todo_id`, `tag_id` | — |
| POST | `/create` | `todo_id` | `TagCreate` |
| PATCH | `/patch` | `tag_id` | `TagPatch` |
| DELETE | `/delete` | `tag_id` | — |

### Comments (`/comments`)
| Method | Path | Query params | Body |
|--------|------|-------------|------|
| GET | `/all` | `todo_id` | — |
| GET | `/item` | `todo_id`, `comment_id` | — |
| POST | `/create` | `todo_id` | `CommentCreate` |
| PUT | `/update` | `todo_id`, `comment_id` | `CommentCreate` |
| DELETE | `/delete` | `comment_id` | — |

## Data Model

Seven ORM models (all inherit `Base` from `db`). `TodoTags` is a join table, not exported from `models/__init__.py`.

- **`User`** — `username`, `email` (unique, indexed), `hashed_password`, `is_active`, `created_at`; relationships: `todos`, `tags`, `refresh_tokens`, `categories`, `comments`
- **`Todo`** — FK→`users.id`, FK→`categories.id` (nullable); `title`, `description` (TEXT), `status` (`Status` enum: todo/done/in_progress), `priority` (`Priority` enum: low/medium/high), `deadline`, `created_at`, `updated_at`
- **`Tag`** — FK→`users.id`, `name`, `color` (String(7), default `#10b981`); unique per user via `UniqueConstraint("user_id", "name")`
- **`TodoTags`** — join table (`todo_id`, `tag_id`) with composite PK
- **`RefreshToken`** — FK→`users.id`, `token` (TEXT, unique, indexed), `expires_at`, `is_revoked`, `created_at`
- **`Category`** — FK→`users.id`, `name`, `color` (String(7)), `created_at`, `updated_at`; `back_populates="user_categories"` on User
- **`Comment`** — FK→`users.id`, FK→`todos.id`, `content` (TEXT), `created_at`, `updated_at`

## Configuration

`app/core/config.py` defines `Settings(BaseSettings)` with fields: `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASS`, `SECRET_KEY`, `ALGORITHM` (default `HS256`), `ACCESS_TOKEN_EXPIRE_MINUTES` (default 30), `REFRESH_TOKEN_EXPIRE_DAYS` (default 30). Reads from `.env` at project root. Exposes `settings` singleton and a `DATABASE_URL` property (returns `postgresql+asyncpg://...` URL).

## Alembic

`alembic/env.py` inserts `app/` into `sys.path`, then imports `from db import Base, DATABASE_URL` and `import models` (triggers all model imports for autogenerate). Sets `sqlalchemy.url` from `DATABASE_URL` at runtime, so `alembic.ini` URL is ignored. Runs async migrations via `asyncio.run(run_async_migrations())`.

## Key Conventions

- **SQLAlchemy 2.x** with `Mapped`/`mapped_column` typed annotations.
- **Import asymmetry**: all internal imports use bare module names (`from db import ...`, `from models import ...`, `from schemas import ...`, `from core import ...`) because `app/` is on `sys.path`. This applies to routers, services, repositories, and alembic env.py.
- All models must be listed in `app/models/__init__.py` for Alembic autogenerate to detect all tables.
- **Session DI**: inject `AsyncSession` via `Depends(get_async_session)` (imported from `db`).
- **`core/__init__.py`** exports: `settings`, `AllError`, `ErrorMessages`, `hash_password`, `verify_password`, `create_access_token`, `create_refresh_token`, `decode_token`, `setup_logging`, `get_logger`. Any new `security.py` or `logging.py` functions must also be re-exported here.
- **`AllError` usage**: it *returns* an HTTPException, so it must be used with `raise`: `raise AllError(ErrorMessages.USER_404).not_found()`.

## Infrastructure

`docker-compose.yml` runs PostgreSQL 16 on port **5433** (maps to container 5432). Credentials: `todo_user`/`todo_pass`, DB `todo_db`. Start with `docker compose up -d`.