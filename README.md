# DRF Homework - Образовательная платформа

## Описание проекта

Образовательная платформа для управления курсами и уроками с возможностью подписки на обновления, возможностью оплаты через  *https://stripe.com/docs/api* и фоновыми задачами через Celery.

### Функциональность

- Управление курсами и уроками (CRUD)
- Подписка пользователей на обновления курсов
- Аутентификация через JWT токены
- Разграничение прав доступа (пользователи, модераторы)
- Фоновые задачи через Celery
- Периодические задачи через Celery Beat
- Валидация YouTube ссылок
- Документация API (Swagger, Redoc)

## Технологии

- Python 3.11
- PostgreSQL
- Django 4.2
- Django REST Framework
- Redis
- Celery
- Docker / Docker Compose
- JWT-Аутентификация

## Требования для запуска

- Docker Desktop (Windows/Mac) или Docker Engine (Linux)
- Git

## Быстрый запуск

### 1. Клонируйте репозиторий

```bash
git clone https://github.com/KuzinaKA85/DRF_homework.git
cd DRF_homework
```
### 2. Настройте переменные окружения
Скопируйте файл .env.example в .env:

```bash
cp .env.example .env
```
Отредактируйте .env, указав свои значения.

### 3. Запустите проект
```bash
docker-compose up -d
```
### 4. Откройте приложение
- API: http://localhost:8000

- Админка: http://localhost:8000/admin

- Swagger документация: http://localhost:8000/swagger/

- Redoc документация: http://localhost:8000/redoc/

### 5. Проверка работоспособности сервисов
5.1 Проверка Web сервиса (Django)
```bash
# Проверить статус контейнера
docker ps | grep web

# Проверить доступность API
curl http://localhost:8000/

# Открыть в браузере
start http://localhost:8000
```
5.2 Проверка PostgreSQL

```bash
# Проверить подключение к БД
docker-compose exec db pg_isready -U postgres

# Ожидаемый ответ: /var/run/postgresql:5432 - accepting connections
```
5.3 Проверка Redis
```bash
# Проверить, что Redis работает
docker-compose exec redis redis-cli ping

# Ожидаемый ответ: PONG
```
5.4 Проверка Celery Worker
```bash
# Проверить статус Celery
docker-compose exec celery poetry run celery -A config status

# Ожидаемый вывод: celery@... OK
```
5.5 Проверка всех сервисов одной командой
```bash
docker-compose ps
```
*Все сервисы должны быть в статусе Up (кроме celery-beat, он может перезапускаться).*

5.6 Остановка проекта
```bash
docker compose down
```
5.7 Остановка проекта с полной очисткой
```bash
docker compose down -v
```

### 6. Переменные окружения
Все чувствительные переменные вынесены в файл .env
- SECRET_KEY=
- DEBUG=
- DATABASE_NAME=
- DATABASE_USER=
- DATABASE_PASSWORD=
- DATABASE_HOST=
- DATABASE_PORT=
- STRIPE_API_KEY=
- CELERY_BROKER_URL=
- CELERY_RESULT_BACKEND=
- EMAIL_HOST_USER=
- EMAIL_HOST_PASSWORD=


### 7. Структура проекта

---
    DRF_homework/
    ├── .venv1/                # Виртуальное окружение (не включается в Git)
    ├── config/                # Настройки проекта
    ├── materials/             # Приложение материалов (курсы, уроки)
    ├── static/                # Статические файлы
    ├── users/                 # Приложение пользователей
    ├── docker-compose.yaml    # Оркестрация сервисов
    ├── Dockerfile             # Инструкция для сборки образа
    ├── .env.example           # Шаблон переменных окружения
    ├── manage.py              # Утилита командной строки Django
    ├── pyproject.toml         # Зависимости Poetry
    └── README.md              # Документация
---

### Важно

В Docker:
- PostgreSQL доступен по хосту `db`
- Redis доступен по хосту `redis`

Использование `localhost` внутри контейнеров не работает.