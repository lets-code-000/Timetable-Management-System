# app/models/user.py
from typing import Optional
from sqlmodel import SQLModel, Field,Relationship

class User(SQLModel, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    email: str = Field(index=True, unique=True)
    phone_number: str | None = Field(default=None, index=True)
    hashed_password: str
    
    token_version: int = Field(default=0, nullable=False)

    role_id: int | None = Field(default=None, foreign_key="roles.id")
    college_id: int | None = Field(default=None, foreign_key="college.id")

    role: "Role" = Relationship(back_populates="users")
    college: "College" = Relationship(back_populates="users")
