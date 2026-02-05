from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session
from app.database import get_db
from app.crud.user import get_user_by_email, verify_password
from app.crud.jwt import create_access_token

router = APIRouter()

@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_db)
):
    user = get_user_by_email(session, form_data.username)

    if not user or not verify_password(
        form_data.password, user.hashed_password
    ):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(
        {
            "sub": user.email,
            "token_version": user.token_version
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
