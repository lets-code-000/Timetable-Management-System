from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship


class College(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True)
    address: Optional[str] = None
    contact: Optional[str] = None

    # Relationships
    departments: List["Department"] = Relationship(back_populates="college")
    classrooms: List["Classroom"] = Relationship(back_populates="college")
    faculties: List["Faculty"] = Relationship(back_populates="college")
    subjects: List["Subject"] = Relationship(back_populates="college")
    users: List["User"] = Relationship(back_populates="college")
    timetables: List["Timetable"] = Relationship(back_populates="college")
