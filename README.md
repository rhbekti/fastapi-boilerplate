# FastAPI Boilerplate

Production-ready REST API template built with FastAPI, SQLModel, PostgreSQL, and Alembic. Uses `uv` for package management.

## Tech Stack

| Library | Role |
|---|---|
| FastAPI | Web framework |
| SQLModel | ORM (SQLAlchemy + Pydantic) |
| PostgreSQL | Database |
| psycopg (v3) | Async DB driver with connection pool |
| Alembic | DB migrations |
| Pydantic Settings | Config from env vars |
| Uvicorn | ASGI server |
| uv | Package manager |

## Features

- **Unified response format** — all successful JSON responses auto-wrapped via middleware: `{ success, message, data }`
- **Global exception handlers** — HTTP, validation, `AlreadyExistsError`, and unhandled exceptions all return consistent JSON
- **Async DB session** — `psycopg` connection pool + SQLAlchemy async engine, initialized at app lifespan
- **Modular structure** — each domain (e.g. `user`) owns its router, service, models, and dependencies
- **Structured logging** — centralized setup via `src/core/logging.py`

## Project Structure

```
fastapi-boilerplate/
├── main.py                    # App entry point, lifespan, middleware, routers
├── alembic.ini                # Alembic config
├── pyproject.toml             # Project metadata and dependencies
├── .env                       # Environment variables (not committed)
├── .env.example               # Env var template
│
├── migrations/                # Alembic migration files
│   ├── env.py
│   ├── script.py.mako
│   └── versions/
│
├── src/
│   ├── core/                  # Shared infrastructure
│   │   ├── config.py          # App config via pydantic-settings
│   │   ├── dependencies.py    # DB engine init, session factory, SessionDep
│   │   ├── exceptions.py      # Custom exceptions + exception handlers
│   │   ├── logging.py         # Logging setup
│   │   ├── middlewares.py     # UnifiedResponseMiddleware
│   │   └── models.py          # IResponse generic response model
│   │
│   └── user/                  # User domain module
│       ├── models.py          # SQLModel table + Pydantic schemas
│       ├── router.py          # CRUD route handlers
│       ├── service.py         # Business logic
│       └── dependencies.py    # UserServiceDep injection
│
└── tests/                     # Pytest test files
```

## Setup

### 1. Clone and install dependencies

```bash
git clone <repo-url>
cd fastapi-boilerplate
uv sync
```

### 2. Configure environment

```bash
cp .env.example .env
# Edit .env — set DATABASE_URL
```

`.env.example`:
```
DATABASE_URL=postgresql://username:password@host:port/db_name
```

### 3. Run migrations

```bash
uv run alembic upgrade head
```

### 4. Run development server

```bash
uv run fastapi dev
```

API docs available at `http://localhost:8000/docs`.

## API Endpoints

### Users — `/users`

| Method | Path | Description |
|---|---|---|
| GET | `/users/` | List users (pagination: `offset`, `limit`) |
| POST | `/users/` | Create user |
| GET | `/users/{id}` | Get user by ID |
| PUT | `/users/{id}` | Update user |
| DELETE | `/users/{id}` | Delete user |

## Response Format

All endpoints return:

```json
{
  "success": true,
  "message": "Operation successful",
  "data": { ... }
}
```

Errors:

```json
{
  "success": false,
  "message": "Error detail",
  "data": null
}
```

## Adding New Modules

1. Create `src/<module>/` with `models.py`, `service.py`, `router.py`, `dependencies.py`
2. Register router in `main.py`:
   ```python
   from src.<module>.router import router as <module>_router
   app.include_router(<module>_router)
   ```
3. Create Alembic migration if new DB table:
   ```bash
   uv run alembic revision --autogenerate -m "add <module> table"
   uv run alembic upgrade head
   ```

## Development

```bash
# Add dependency
uv add <package>

# Add dev dependency
uv add --dev <package>

# Run tests
uv run pytest
```
