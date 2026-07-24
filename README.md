# Task Manager API on FastAPI

## Описание
REST API для управления задачами с аутентификацией. Проект создан для изучения FastAPI и построения бэкенда для пет-проекта.

## Технологии
- **FastAPI** — современный веб-фреймворк для Python
- **SQLAlchemy** — ORM для работы с базами данных
- **SQLite** — легкая база данных (в будущем заменим на PostgreSQL)
- **JWT** — аутентификация (будет добавлена)
- **Alembic** — миграции базы данных
- **Docker** — контейнеризация (в будущем)

## Установка и запуск

### 1. Клонирование репозитория
```bash
git clone https://github.com/AndreiZhiburtovich/task-manager-fastapi.git
cd task-manager-fastapi
```

### 2. Создание виртуального окружения
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows
```

### 3. Установка зависимостей
```bash
pip install -r requirements.txt
```

### 4. Запуск приложения
```bash
python run.py
```

После запуска сервер будет доступен по адресу: http://localhost:8000

## Документация API

После запуска приложения документация доступна по адресам:
- **Swagger UI** — http://localhost:8000/docs
- **ReDoc** — http://localhost:8000/redoc

## API Endpoints

| Метод | Эндпоинт | Описание |
|-------|----------|----------|
| GET | `/` | Проверка работы API |
| GET | `/tasks` | Получить список всех задач |
| GET | `/tasks/{id}` | Получить задачу по ID |
| POST | `/tasks` | Создать новую задачу |
| PUT | `/tasks/{id}` | Обновить задачу |
| DELETE | `/tasks/{id}` | Удалить задачу |

### Пример запроса (POST /tasks)
```json
{
  "title": "Изучить FastAPI",
  "description": "Полностью изучить документацию FastAPI",
  "completed": false
}
```

### Пример ответа
```json
{
  "id": 1,
  "title": "Изучить FastAPI",
  "description": "Полностью изучить документацию FastAPI",
  "completed": false,
  "created_at": "2024-01-15T10:00:00",
  "updated_at": null
}
```

## Структура проекта

```
task-manager-fastapi/
├── app/
│   ├── __init__.py          # Инициализация пакета
│   ├── main.py              # Точка входа в приложение
│   ├── database.py          # Настройка подключения к БД
│   ├── models.py            # Модели SQLAlchemy
│   ├── schemas.py           # Схемы Pydantic для валидации
│   ├── crud.py              # CRUD операции с БД
│   ├── auth.py              # Аутентификация (JWT)
│   └── routes.py            # API эндпоинты
├── venv/                    # Виртуальное окружение
├── requirements.txt         # Зависимости проекта
├── run.py                   # Файл для запуска приложения
├── .gitignore               # Игнорируемые файлы
└── README.md                # Описание проекта
```

## Планы по развитию

- [x] Базовая структура проекта
- [x] Модель Task с CRUD операциями
- [x] Swagger документация
- [ ] Аутентификация (JWT)
- [ ] Модель User (регистрация, логин)
- [ ] Связь задач с пользователями
- [ ] Фронтенд на React
- [ ] Деплой на сервер
- [ ] Docker контейнеризация

## Команды для работы с Git

```bash
git status          # Проверить статус
git add .           # Добавить все изменения
git commit -m "..." # Сохранить изменения
git push            # Отправить на GitHub
git pull            # Получить обновления
```

## Лицензия
MIT

## Автор
**Andrei Zhiburtovich**
- GitHub: [@AndreiZhiburtovich](https://github.com/AndreiZhiburtovich)

---

⭐ Если вам понравился проект, поставьте звезду на GitHub!
