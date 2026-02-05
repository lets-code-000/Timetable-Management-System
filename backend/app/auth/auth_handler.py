# app/auth/auth_handler.py
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.database import get_db
from app.crud.user import get_user_by_email, verify_password
from app.crud.jwt import create_access_token

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/login")
def login(email: str, password: str, session: Session = Depends(get_db)):
    user = get_user_by_email(session, email)

    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(
        data={
            "sub": user.email,
            "token_version": user.token_version
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
