from sqlalchemy.orm import Session
from app import models, schemas
from app.auth import get_password_hash

# ----- Task CRUD -----
def get_task(db: Session, task_id: int, user_id: int):
    """Получить задачу по ID (только для конкретного пользователя)"""
    return db.query(models.Task).filter(
        models.Task.id == task_id,
        models.Task.user_id == user_id
    ).first()

def get_tasks(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    """Получить все задачи пользователя с пагинацией"""
    return db.query(models.Task).filter(
        models.Task.user_id == user_id
    ).offset(skip).limit(limit).all()

def create_task(db: Session, task: schemas.TaskCreate, user_id: int):
    """Создать новую задачу для пользователя"""
    db_task = models.Task(**task.model_dump(), user_id=user_id)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def update_task(db: Session, task_id: int, task_update: schemas.TaskUpdate, user_id: int):
    """Обновить задачу (только для конкретного пользователя)"""
    db_task = get_task(db, task_id, user_id)
    if db_task:
        for key, value in task_update.model_dump(exclude_unset=True).items():
            setattr(db_task, key, value)
        db.commit()
        db.refresh(db_task)
    return db_task

def delete_task(db: Session, task_id: int, user_id: int):
    """Удалить задачу (только для конкретного пользователя)"""
    db_task = get_task(db, task_id, user_id)
    if db_task:
        db.delete(db_task)
        db.commit()
        return True
    return False

# ----- User CRUD -----
def get_user_by_username(db: Session, username: str):
    """Получить пользователя по username"""
    return db.query(models.User).filter(models.User.username == username).first()

def get_user_by_email(db: Session, email: str):
    """Получить пользователя по email"""
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    """Создать нового пользователя (с хешированием пароля)"""
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
