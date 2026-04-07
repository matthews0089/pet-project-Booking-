# Copilot / AI Agent Instructions (concise)

This repository is a small FastAPI service using SQLAlchemy (async) and a DAO pattern. Keep guidance short and specific to help contributors and AI assistants be productive immediately.

- **Project entry:** FastAPI app created in [app/main.py](app/main.py). Include routers via `app.include_router(...)` (see [app/bookings/router.py](app/bookings/router.py)).
- **Database:** Async SQLAlchemy engine and session factory live in [app/database.py](app/database.py). Use `async_session_maker()` for async DB sessions.
- **Models:** Domain models live per-module under `app/<domain>/models.py` (example: [app/bookings/models.py](app/bookings/models.py)). Models inherit from `app.database.Base` and may include SQL `Computed` columns (e.g., `total_cost`, `total_days`).
- **DAO pattern:** Data access uses a base DAO at [dao/base.py](dao/base.py). Subclasses (e.g., `BookingDAO` at [app/bookings/dao.py](app/bookings/dao.py)) set a `model` attribute and call `async` classmethods such as `find_by_id`.

Key conventions and patterns to follow when editing or generating code:

- Use async DB sessions. Example pattern:

  - `async with async_session_maker() as session:`
  - Build queries with `select(Model).filter_by(...)` and `await session.execute(query)` (see [dao/base.py](dao/base.py)).

- DAO methods are `@classmethod` and `async`. When creating new DAOs, set `model = YourModel` and reuse patterns from `BookingDAO`.

- Routers are simple and return DAO results directly in existing code (e.g., `BookingDAO.find_by_id(1)` in [app/bookings/router.py](app/bookings/router.py)). Be conservative when changing return types — existing handlers rely on SQLAlchemy model instances.

- Keep imports using package form `from app...` to match runtime package layout.

Migrations and development commands:

- Alembic configs exist (see `alembic.ini` and migration folders under `app/migrations/` and top-level `migrations/`). Typical commands (run from repo root):

  - `alembic -c alembic.ini upgrade head` — apply migrations
  - `alembic -c alembic.ini revision --autogenerate -m "msg"` — create migration

- Run the API locally with Uvicorn: `uvicorn app.main:app --reload` (working dir: repo root).

What an AI assistant should do (concrete):

- When asked to add a new endpoint, create `router.py` in the domain folder, export `router = APIRouter(...)`, and include it in [app/main.py](app/main.py).
- When changing DB logic, update or add a DAO under `dao/` or `app/<domain>/dao.py` following `BaseDAO` patterns and use `async_session_maker`.
- When adding models, inherit from `app.database.Base` and put them in `app/<domain>/models.py`.

Files to check first for context on changes:

- [app/main.py](app/main.py)
- [app/database.py](app/database.py)
- [dao/base.py](dao/base.py)
- [app/bookings/models.py](app/bookings/models.py)
- [app/bookings/dao.py](app/bookings/dao.py)
- [app/bookings/router.py](app/bookings/router.py)

If anything is unclear or you need additional conventions (tests, linting, or CI commands), ask and I will update this file. Please review and tell me what to expand or change.
