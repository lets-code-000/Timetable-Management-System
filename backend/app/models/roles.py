from typing import Optional
from sqlmodel import SQLModel, Field, Relationship


class Role(SQLModel, table=True):
    __tablename__ = "roles"

    id: Optional[int] = Field(default=None, primary_key=True)
    role_name: str = Field(index=True, unique=True)

    users: list["User"] = Relationship(back_populates="role")