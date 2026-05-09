# apps/api — Backend Conventions

- Async SQLAlchemy everywhere — never use sync sessions or `db.execute()` with non-async engine
- Routers are HTTP-only: no business logic, no direct DB queries — delegate to `services/`
- All Quran Foundation API calls go through `services/quran_service.py` only
- Use Pydantic v2 models for all schemas
- Every endpoint requires `get_current_user_id` dependency
- Tests live in `tests/` and cover the service layer
