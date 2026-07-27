import pytest
from app.models import User
from app.database import SessionLocal


def test_create_task(client, auth_headers):
    """Тест: создание новой задачи."""
    print(f"Auth headers: {auth_headers}")
    
    response = client.post("/tasks", json={
        "title": "Test Task",
        "description": "Test Description",
        "completed": False
    }, headers=auth_headers)
    
    print(f"Response status: {response.status_code}")
    print(f"Response body: {response.text}")
    
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Task"
    assert data["description"] == "Test Description"
    assert data["completed"] == False
    assert "id" in data
    assert "user_id" in data


def test_create_task_without_title(client, auth_headers):
    """Тест: создание задачи без заголовка (должно вернуть ошибку)."""
    response = client.post("/tasks", json={
        "description": "Test Description",
        "completed": False
    }, headers=auth_headers)
    
    print(f"Response status: {response.status_code}")
    print(f"Response body: {response.text}")
    
    assert response.status_code == 422


def test_get_tasks_empty(client, auth_headers):
    """Тест: получение списка задач (пустой список)."""
    response = client.get("/tasks", headers=auth_headers)
    assert response.status_code == 200
    assert response.json() == []


def test_get_tasks_with_data(client, auth_headers):
    """Тест: получение списка задач (с данными)."""
    # Создаём задачу
    client.post("/tasks", json={
        "title": "Task 1",
        "description": "Description 1",
        "completed": False
    }, headers=auth_headers)
    
    # Получаем список
    response = client.get("/tasks", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["title"] == "Task 1"


def test_get_task_by_id(client, auth_headers):
    """Тест: получение задачи по ID."""
    # Создаём задачу
    create_response = client.post("/tasks", json={
        "title": "Task for ID",
        "description": "Description",
        "completed": False
    }, headers=auth_headers)
    
    task_id = create_response.json()["id"]
    
    # Получаем задачу по ID
    response = client.get(f"/tasks/{task_id}", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == task_id
    assert data["title"] == "Task for ID"


def test_get_task_not_found(client, auth_headers):
    """Тест: получение несуществующей задачи."""
    response = client.get("/tasks/9999", headers=auth_headers)
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_update_task(client, auth_headers):
    """Тест: обновление задачи."""
    # Создаём задачу
    create_response = client.post("/tasks", json={
        "title": "Old Title",
        "description": "Old Description",
        "completed": False
    }, headers=auth_headers)
    
    task_id = create_response.json()["id"]
    
    # Обновляем задачу
    response = client.put(f"/tasks/{task_id}", json={
        "title": "New Title",
        "completed": True
    }, headers=auth_headers)
    
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "New Title"
    assert data["description"] == "Old Description"
    assert data["completed"] == True


def test_delete_task(client, auth_headers):
    """Тест: удаление задачи."""
    # Создаём задачу
    create_response = client.post("/tasks", json={
        "title": "Task to Delete",
        "description": "Description",
        "completed": False
    }, headers=auth_headers)
    
    task_id = create_response.json()["id"]
    
    # Удаляем задачу
    response = client.delete(f"/tasks/{task_id}", headers=auth_headers)
    assert response.status_code == 200
    assert "Task deleted" in response.json()["message"]
    
    # Проверяем, что задача действительно удалена
    get_response = client.get(f"/tasks/{task_id}", headers=auth_headers)
    assert get_response.status_code == 404


def test_unauthorized_access(client):
    """Тест: доступ к защищённому эндпоинту без токена."""
    response = client.get("/tasks")
    assert response.status_code == 401
    assert "not authenticated" in response.json()["detail"].lower()
