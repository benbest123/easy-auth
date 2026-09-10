dev:
    docker compose start
    uv run fastapi dev src/easy_auth/main.py

test:
    uv run pytest

check:
    uv run ruff check . && uv run ruff format --check . && uv run mypy src tests && uv run pytest

migrate:
    uv run alembic upgrade head