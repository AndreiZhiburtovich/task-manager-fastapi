# Task Manager API on FastAPI

## Описание
REST API для управления задачами с аутентификацией.

## Технологии
- FastAPI
- SQLAlchemy (ORM)
- PostgreSQL (база данных)
- JWT (аутентификация)
- Alembic (миграции)
- Docker (контейнеризация)

## Установка

```bash
# Клонирование
git clone https://github.com/AndreiZhiburtovich/task-manager-fastapi.git
cd task-manager-fastapi

# Виртуальное окружение
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Установка зависимостей
pip install -r requirements.txt

# Запуск
uvicorn main:app --reload

