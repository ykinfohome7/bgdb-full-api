from datetime import datetime, timedelta
from typing import Optional, Any, Union
from jose import jwt
from passlib.context import CryptContext
from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_token(subject: Union[str, Any], expires_delta: timedelta, token_type: str = "access") -> str:
    now = datetime.utcnow()
    to_encode = {"exp": now + expires_delta, "iat": now, "sub": str(subject), "type": token_type}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def create_access_token(subject: Union[str, Any]) -> str:
    return create_token(subject, timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES), "access")

def create_refresh_token(subject: Union[str, Any]) -> str:
    return create_token(subject, timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES), "refresh")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)
