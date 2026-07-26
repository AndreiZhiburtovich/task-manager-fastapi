import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

# Читаем DATABASE_URL с проверкой
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError(
        "DATABASE_URL is not set! "
        "Please create .env file with DATABASE_URL=sqlite:///./task_manager.db"
    )

# Создаём движок базы данных
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}  # Только для SQLite
)

# Создаём фабрику сессий
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Базовый класс для моделей
Base = declarative_base()


def get_db():
    """Генератор сессии базы данных для Dependency Injection."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
