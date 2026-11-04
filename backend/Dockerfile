FROM python:3.13-slim
WORKDIR /usr/local/app

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
COPY pyproject.toml ./
COPY uv.lock ./

RUN uv sync --frozen --no-dev

ENV PATH="/usr/local/app/.venv/bin:$PATH"

COPY /app ./app/
COPY /migrations ./migrations/
COPY alembic.ini ./

RUN useradd app
USER app

EXPOSE 8000

CMD ["sh", "-c", "alembic upgrade head && fastapi run app/main.py --host 0.0.0.0 --port 8000"]

