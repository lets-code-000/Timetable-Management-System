from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session
from app.database import get_db
from .jwt import decode_access_token
from .user import get_user_by_username, get_user_by_email

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_db)
):
    payload = decode_access_token(token)

    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    email = payload.get("sub")
    token_version = payload.get("token_version")

    if email is None or token_version is None:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = get_user_by_email(session, email)

    if not user:
        raise HTTPException(status_code=401, detail="User no longer exists")

    if user.token_version != token_version:
        raise HTTPException(status_code=401, detail="Token revoked")

    return user
