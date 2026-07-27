import os
from datetime import datetime, timedelta
from typing import Optional

from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import User
from app.schemas import TokenData

# Загружаем переменные окружения
load_dotenv()


# --- Конфигурация ---
def _get_env_var(name: str, default: Optional[str] = None) -> str:
    """Получает переменную окружения с проверкой."""
    value = os.getenv(name, default)
    if value is None:
        raise ValueError(
            f"{name} is not set! "
            f"Please create .env file with {name}=your-value"
        )
    return value


SECRET_KEY = _get_env_var("SECRET_KEY")
ALGORITHM = _get_env_var("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(_get_env_var("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))


# --- Настройки хеширования и OAuth2 ---
pwd_context = CryptContext(schemes=["sha256_crypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_db():
    """Генератор сессии базы данных."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Проверяет, соответствует ли пароль хешу."""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Хеширует пароль."""
    return pwd_context.hash(password)


def authenticate_user(db: Session, username: str, password: str) -> Optional[User]:
    """Аутентифицирует пользователя по логину и паролю."""
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Создаёт JWT токен."""
    to_encode = data.copy()
    # Используем datetime.utcnow() для совместимости с Python 3.11 и ниже
    expire = datetime.utcnow() + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    """Получает текущего пользователя по JWT токену."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if not username:
            raise credentials_exception
        
        user = db.query(User).filter(User.username == username).first()
        if not user:
            raise credentials_exception
        return user
    except JWTError:
        raise credentials_exception


async def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """Проверяет, активен ли текущий пользователь."""
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
