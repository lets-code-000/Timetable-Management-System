# app/routes/auth.py
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.database import get_db
from app.schemas.user import UserCreate, UserOut
from app.crud.user import (
    get_user_by_username,
    create_user,
    verify_password,
    get_user_by_email,
)
from app.crud.jwt import create_access_token


from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends

router = APIRouter()


@router.post("/register", response_model=UserOut)
def register(user: UserCreate, session: Session = Depends(get_db)):
    db_user = get_user_by_username(session, user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    if get_user_by_email(session, user.email):
        raise HTTPException(status_code=400, detail="Email already registered")

    return create_user(session, user)


@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_db)
):
    db_user = get_user_by_email(session, form_data.username)

    if not db_user or not verify_password(form_data.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(
        {"sub": db_user.email, "token_version": db_user.token_version}
    )

    return {"access_token": access_token, "token_type": "bearer"}
