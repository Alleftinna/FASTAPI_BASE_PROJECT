FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update \
    && apt-get install -y gcc netcat-traditional \
    && pip install poetry \
    && apt-get purge -y --auto-remove \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml ./
RUN poetry config virtualenvs.create false \
    && poetry lock \
    && poetry install --with dev --no-interaction --no-ansi --no-root

COPY . .

ADD https://storage.yandexcloud.net/cloud-certs/CA.pem /usr/local/share/ca-certificates/YandexCA.crt
RUN update-ca-certificates \
    chmod +x /app/docker/scripts/start-bot.sh

