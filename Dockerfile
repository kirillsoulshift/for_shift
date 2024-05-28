# syntax=docker/dockerfile:1
FROM python:3.12-alpine as base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"

RUN apk update && apk add libpq

FROM base as builder

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

RUN apk update && \
    apk add musl-dev build-base gcc gfortran openblas-dev

WORKDIR /app

RUN pip install poetry==1.8.3

COPY pyproject.toml poetry.lock ./

RUN poetry install

FROM base as runtime

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

COPY . ./src

WORKDIR /app/src

ENTRYPOINT ["poetry", "run", "python3", "main.py"]
