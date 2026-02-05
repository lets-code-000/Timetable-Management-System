# app/crud/jwt.py
from datetime import datetime, timedelta
from jose import JWTError, jwt
from uuid import uuid4
from app.config import settings

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (
        expires_delta or timedelta(minutes=15)
    )
    to_encode.update({
        "exp": expire,
        "jti": str(uuid4())
    })
    return jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )

def decode_access_token(token: str) -> dict | None:
    try:
        return jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
    except JWTError:
        return None
