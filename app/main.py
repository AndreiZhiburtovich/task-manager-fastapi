from fastapi import FastAPI
from app.routes import router

app = FastAPI(
    title="Task Manager API",
    description="API для управления задачами",
    version="1.0.0"
)

# Подключаем роуты
app.include_router(router)

@app.get("/")
def root():
    return {
        "message": "Task Manager API is running!",
        "docs": "/docs",
        "redoc": "/redoc"
    }

