# Task Manager API on FastAPI

## Описание
REST API для управления задачами с JWT аутентификацией. Проект создан для изучения FastAPI и построения бэкенда для пет-проекта.

## Технологии
- **FastAPI** — современный веб-фреймворк для Python
- **SQLAlchemy** — ORM для работы с базами данных
- **SQLite** — легкая база данных (в будущем заменим на PostgreSQL)
- **JWT** — аутентификация через JSON Web Tokens
- **bcrypt** — хеширование паролей
- **Pydantic** — валидация данных
- **Uvicorn** — ASGI сервер
- **Alembic** — миграции базы данных
- **python-dotenv** — управление переменными окружения

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

### 4. Настройка переменных окружения

Создайте файл `.env` в корне проекта на основе `.env.example`:

```bash
cp .env.example .env
```

Отредактируйте `.env` и укажите свои значения:

```bash
SECRET_KEY=your-super-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
DATABASE_URL=sqlite:///./task_manager.db
```

> **Важно:** Никогда не коммитьте `.env` файл в репозиторий! Он содержит секретные ключи.

### 5. Применение миграций базы данных
```bash
alembic upgrade head
```

### 6. Запуск приложения
```bash
python run.py
```

После запуска сервер будет доступен по адресу: http://localhost:8000

## Документация API

После запуска приложения документация доступна по адресам:
- **Swagger UI** — http://localhost:8000/docs
- **ReDoc** — http://localhost:8000/redoc

## API Endpoints

### Публичные эндпоинты (без авторизации)

| Метод | Эндпоинт | Описание |
|-------|----------|----------|
| GET | `/` | Проверка работы API |
| GET | `/health` | Проверка состояния сервиса |
| POST | `/register` | Регистрация нового пользователя |
| POST | `/token` | Получение JWT токена |

### Защищённые эндпоинты (требуется JWT токен)

| Метод | Эндпоинт | Описание |
|-------|----------|----------|
| GET | `/tasks` | Получить список всех задач пользователя |
| GET | `/tasks/{id}` | Получить задачу по ID |
| POST | `/tasks` | Создать новую задачу |
| PUT | `/tasks/{id}` | Обновить задачу |
| DELETE | `/tasks/{id}` | Удалить задачу |

## Примеры запросов

### Регистрация пользователя
```http
POST /register
Content-Type: application/json

{
  "username": "testuser",
  "email": "test@example.com",
  "password": "securepassword123"
}
```

### Получение токена
```http
POST /token
Content-Type: application/x-www-form-urlencoded

username=testuser&password=securepassword123
```

**Ответ:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### Создание задачи (с токеном)
```http
POST /tasks
Authorization: Bearer YOUR_ACCESS_TOKEN
Content-Type: application/json

{
  "title": "Изучить FastAPI",
  "description": "Полностью изучить документацию FastAPI",
  "completed": false
}
```

**Ответ:**
```json
{
  "id": 1,
  "title": "Изучить FastAPI",
  "description": "Полностью изучить документацию FastAPI",
  "completed": false,
  "created_at": "2024-01-15T10:00:00",
  "updated_at": null,
  "user_id": 1
}
```

### Получение всех задач (с токеном)
```http
GET /tasks
Authorization: Bearer YOUR_ACCESS_TOKEN
```

**Ответ:**
```json
[
  {
    "id": 1,
    "title": "Изучить FastAPI",
    "description": "Полностью изучить документацию FastAPI",
    "completed": false,
    "created_at": "2024-01-15T10:00:00",
    "updated_at": null,
    "user_id": 1
  }
]
```

### Обновление задачи (с токеном)
```http
PUT /tasks/1
Authorization: Bearer YOUR_ACCESS_TOKEN
Content-Type: application/json

{
  "completed": true
}
```

### Удаление задачи (с токеном)
```http
DELETE /tasks/1
Authorization: Bearer YOUR_ACCESS_TOKEN
```

## Аутентификация

Проект использует JWT (JSON Web Tokens) для аутентификации:

1. **Регистрация** — создание нового пользователя
2. **Логин** — получение JWT токена через `/token`
3. **Доступ к защищённым эндпоинтам** — передача токена в заголовке `Authorization: Bearer <token>`

Токен действителен **30 минут** (настраивается в `.env`). По истечении срока нужно получить новый.

## Переменные окружения

Проект использует файл `.env` для управления настройками. Обязательные переменные:

| Переменная | Описание | Пример |
|------------|----------|--------|
| `SECRET_KEY` | Секретный ключ для JWT (сгенерируйте свой) | `your-super-secret-key` |
| `ALGORITHM` | Алгоритм шифрования JWT | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Время жизни токена в минутах | `30` |
| `DATABASE_URL` | URL для подключения к БД | `sqlite:///./task_manager.db` |

### Генерация SECRET_KEY

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"

## Структура проекта

```
task-manager-fastapi/
├── app/
│   ├── __init__.py          # Инициализация пакета
│   ├── main.py              # Точка входа в приложение
│   ├── database.py          # Настройка подключения к БД
│   ├── models.py            # Модели SQLAlchemy (User, Task)
│   ├── schemas.py           # Схемы Pydantic для валидации
│   ├── crud.py              # CRUD операции с БД
│   ├── auth.py              # JWT аутентификация
│   └── routes.py            # API эндпоинты
├── alembic/                 # Миграции базы данных
│   ├── versions/            # Файлы миграций
│   ├── env.py               # Настройка Alembic
│   └── script.py.mako       # Шаблон для миграций
├── .env                     # Переменные окружения (НЕ В GIT!)
├── .env.example             # Пример переменных окружения
├── venv/                    # Виртуальное окружение
├── requirements.txt         # Зависимости проекта
├── alembic.ini              # Конфигурация Alembic
├── run.py                   # Файл для запуска приложения
├── .gitignore               # Игнорируемые файлы
└── README.md                # Описание проекта
```

## Управление миграциями (Alembic)

### Создание новой миграции
```bash
alembic revision --autogenerate -m "Описание изменений"
```

### Применение миграций
```bash
alembic upgrade head
```

### Откат миграции
```bash
alembic downgrade -1
```

### Просмотр текущего состояния
```bash
alembic current
```

## Планы по развитию

- [x] Базовая структура проекта
- [x] Модель Task с CRUD операциями
- [x] Swagger документация
- [x] Аутентификация (JWT)
- [x] Модель User (регистрация, логин)
- [x] Связь задач с пользователями
- [x] Alembic миграции
- [x] Переменные окружения (.env)
- [ ] Тесты (pytest)
- [ ] Переход на PostgreSQL
- [ ] Docker контейнеризация
- [ ] Фронтенд на React
- [ ] Деплой на сервер

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