import pytest
from app.models import User
from app.database import SessionLocal


def test_root_endpoint(client):
    """Тест: корневой эндпоинт должен возвращать приветствие."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Task Manager API"
    assert data["status"] == "running"


def test_health_check(client):
    """Тест: эндпоинт /health должен возвращать статус OK."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["message"] == "Task Manager API is running"


def test_register_success(client, test_user):
    """Тест: успешная регистрация нового пользователя."""
    response = client.post("/register", json={
        "username": test_user["username"],
        "email": test_user["email"],
        "password": test_user["password"]
    })
    
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == test_user["username"]
    assert data["email"] == test_user["email"]
    assert "id" in data
    assert "hashed_password" not in data


def test_register_duplicate_username(client, test_user):
    """Тест: попытка регистрации с существующим username."""
    # Первая регистрация
    client.post("/register", json={
        "username": test_user["username"],
        "email": test_user["email"],
        "password": test_user["password"]
    })
    
    # Вторая регистрация с тем же username
    response = client.post("/register", json={
        "username": test_user["username"],
        "email": "another@example.com",
        "password": "anotherpass"
    })
    
    assert response.status_code == 400
    assert "already registered" in response.json()["detail"].lower()


def test_register_duplicate_email(client, test_user):
    """Тест: попытка регистрации с существующим email."""
    # Первая регистрация
    client.post("/register", json={
        "username": test_user["username"],
        "email": test_user["email"],
        "password": test_user["password"]
    })
    
    # Вторая регистрация с тем же email
    response = client.post("/register", json={
        "username": "anotheruser",
        "email": test_user["email"],
        "password": "anotherpass"
    })
    
    assert response.status_code == 400
    assert "already registered" in response.json()["detail"].lower()


def test_login_success(client, test_user):
    """Тест: успешный логин и получение токена."""
    # Сначала регистрируем пользователя
    client.post("/register", json={
        "username": test_user["username"],
        "email": test_user["email"],
        "password": test_user["password"]
    })
    
    # Логин
    response = client.post("/token", data={
        "username": test_user["username"],
        "password": test_user["password"]
    })
    
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password(client, test_user):
    """Тест: логин с неправильным паролем."""
    # Сначала регистрируем пользователя
    client.post("/register", json={
        "username": test_user["username"],
        "email": test_user["email"],
        "password": test_user["password"]
    })
    
    # Логин с неправильным паролем
    response = client.post("/token", data={
        "username": test_user["username"],
        "password": "wrongpassword"
    })
    
    assert response.status_code == 401
    assert "incorrect" in response.json()["detail"].lower()


def test_login_nonexistent_user(client):
    """Тест: логин с несуществующим пользователем."""
    response = client.post("/token", data={
        "username": "nonexistent",
        "password": "password"
    })
    
    assert response.status_code == 401
    assert "incorrect" in response.json()["detail"].lower()
