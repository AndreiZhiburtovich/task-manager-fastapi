from fastapi import FastAPI
from app.database import engine, Base
from app.routes import router

# Создаём таблицы в базе данных
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Task Manager API",
    description="REST API for task management with JWT authentication",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Подключаем все маршруты
app.include_router(router)

@app.get("/health")
def health_check():
    """Проверка состояния сервиса"""
    return {"status": "healthy", "message": "Task Manager API is running"}

