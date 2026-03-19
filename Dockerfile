FROM python:3.14-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV POETRY_VERSION=1.8.3

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends curl \
    && pip install "poetry==$POETRY_VERSION" \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

ARG INSTALL_DEV=false

COPY pyproject.toml ./
RUN poetry config virtualenvs.create false \
    && if [ "$INSTALL_DEV" = "true" ]; then poetry install --with dev --no-interaction --no-ansi --no-root; else poetry install --only main --no-interaction --no-ansi --no-root; fi

COPY . .

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]

