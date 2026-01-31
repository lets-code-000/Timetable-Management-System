from typing import Optional
from sqlmodel import SQLModel


class CollegeCreate(SQLModel):
    name: str
    address: Optional[str] = None
    contact: Optional[str] = None


class CollegeUpdate(SQLModel):
    name: Optional[str] = None
    address: Optional[str] = None
    contact: Optional[str] = None


class CollegeRead(SQLModel):
    id: int
    name: str
    address: Optional[str] = None
    contact: Optional[str] = None

    class Config:
        from_attributes = True


class DeleteCollegeResponse(SQLModel):
    message: str
    data: CollegeRead | None = None
