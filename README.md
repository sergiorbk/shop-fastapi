# Лабораторна робота №0: Підготовка застосунку — Readiness & Standardization

## Налаштування

### Змінні оточення

| Змінна | Опис | Приклад |
|--------|------|---------|
| `DB_HOST` | Хост бази даних | `localhost` |
| `DB_PORT` | Порт бази даних | `5433` |
| `DB_NAME` | Назва бази даних | `ecommerce` |
| `DB_USER` | Користувач БД | `postgres` |
| `DB_PASSWORD` | Пароль БД | `postgres` |

### Запуск

```bash
# Встановлення залежностей
uv sync --all-extras

# Запуск тестів (без БД)
uv run pytest

# Запуск застосунку (потребує PostgreSQL)
uv run uvicorn main:app --host localhost --port 8080
```

---

## Фаза 1: Обов'язкові вимоги

### 1. One-Command Build
- Файл залежностей: `pyproject.toml`
- Команда тестів: `uv run pytest`

### 2. Конфігурація через ENV
Всі налаштування зчитуються зі змінних оточення через `pydantic-settings`.

### 3. Автоматичні міграції
Alembic міграції застосовуються автоматично при запуску застосунку.

---

## Фаза 2: Production-Grade фічі

### 1. Health Check

**200 OK** (БД доступна):

![Health Check 200](docs/images/lab0/health-200.png)

**503 Service Unavailable** (БД недоступна):

![Health Check 503](docs/images/lab0/health-503.png)

---

### 2. JSON Logging

Приклад логів при запуску:

![Startup logs](docs/images/lab0/startup-logs.png)

---

### 3. Graceful Shutdown

Після надсилання `SIGTERM` (Ctrl+C):

![Graceful Shutdown](docs/images/lab0/graceful-shutdown.png)

---

### 4. Тестування

Результат виконання тестів:

![Tests](docs/images/lab0/tests.png)

---