from sqlmodel import Session, select
from app.models.user import User
from app.schemas.user import UserCreate
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def get_user_by_username(db: Session, username: str):
    statement = select(User).where(User.username == username)
    result = db.exec(statement).first()
    return result

def create_user(db: Session, user: UserCreate, role_id: int | None = None, college_id: int | None = None):
    # Argon2 doesn't have the 72-byte limitation, so we can hash the full password
    hashed_password = pwd_context.hash(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        phone_number=user.phone_number,
        hashed_password=hashed_password,
        role_id=role_id,
        college_id=college_id
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def verify_password(plain_password, hashed_password):
    # Argon2 can handle full password without truncation
    return pwd_context.verify(plain_password, hashed_password)
def get_user_by_email(session: Session, email: str):
    statement = select(User).where(User.email == email)
    return session.exec(statement).first()