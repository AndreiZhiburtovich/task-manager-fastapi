import os
import sys
from pathlib import Path

# Добавляем путь к корню проекта
sys.path.insert(0, str(Path(__file__).parent.parent))

# Устанавливаем тестовые переменные окружения ДО импорта app
os.environ["SECRET_KEY"] = "test-secret-key-for-tests-only"
os.environ["ALGORITHM"] = "HS256"
os.environ["ACCESS_TOKEN_EXPIRE_MINUTES"] = "9999"
os.environ["DATABASE_URL"] = "sqlite:///./test.db"

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import Base, get_db

# Проверяем, что SECRET_KEY загружен
print(f"SECRET_KEY in tests: {os.getenv('SECRET_KEY')}")

# Создаём тестовую БД
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def test_user():
    return {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpass123"
    }


@pytest.fixture
def auth_token(client, test_user):
    response = client.post("/token", data={
        "username": test_user["username"],
        "password": test_user["password"]
    })
    
    if response.status_code != 200:
        client.post("/register", json={
            "username": test_user["username"],
            "email": test_user["email"],
            "password": test_user["password"]
        })
        response = client.post("/token", data={
            "username": test_user["username"],
            "password": test_user["password"]
        })
    
    assert response.status_code == 200, f"Auth failed: {response.text}"
    return response.json()["access_token"]


@pytest.fixture
def auth_headers(auth_token):
    return {"Authorization": f"Bearer {auth_token}"}
