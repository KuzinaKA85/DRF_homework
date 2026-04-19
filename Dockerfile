# Используем официальный slim-образ Python 3.12
FROM python:3.12-slim

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Устанавливаем зависимости системы
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Добавляем Poetry в PATH
ENV PATH="/root/.local/bin:$PATH"

# Копируем pyproject.toml и poetry.lock для установки зависимостей
COPY pyproject.toml poetry.lock ./

# Устанавливаем зависимости Python с помощью Poetry
RUN poetry install --no-root

# Копируем исходный код приложения в контейнер
COPY . .

# # Определяем переменные окружения
# ENV SECRET_KEY="SECRET_KEY"
# ENV CELERY_BROKER_URL="CELERY_BROKER_URL"
# ENV CELERY_BACKEND="CELERY_RESULT_BACKEND"

# Создаем директорию для медиафайлов
RUN mkdir -p /app/media

# Пробрасываем порт, который будет использовать Django
EXPOSE 8000

# Команда для запуска приложения
CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]