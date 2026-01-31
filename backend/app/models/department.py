from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship


class Department(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    year: int
    college_id: Optional[int] = Field(default=None, foreign_key="college.id")

    # Relationships
    college: "College" = Relationship(back_populates="departments")
    classrooms: List["Classroom"] = Relationship(back_populates="department")
    faculties: List["Faculty"] = Relationship()
    subjects: List["Subject"] = Relationship()
