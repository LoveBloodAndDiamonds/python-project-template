FROM python:3.12-slim

# Определяем рабочую директорию
WORKDIR /app

# Устанавливаем git и системные зависимости
# RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# Устанавливаем uv
RUN pip install --no-cache-dir uv

# Копируем зависимости
COPY uv.lock pyproject.toml /app/

# Устанавилваем зависимости
RUN uv sync

# Копируем приложение
COPY app /app/app
