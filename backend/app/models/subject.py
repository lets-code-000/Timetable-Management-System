from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship


class Subject(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    faculty_id: int = Field(foreign_key="faculty.id")
    department_id: int = Field(foreign_key="department.id")
    college_id: Optional[int] = Field(default=None, foreign_key="college.id")

    faculty: "Faculty" = Relationship()
    department: "Department" = Relationship()
    college: "College" = Relationship(back_populates="subjects")
    slots: List["TimetableSlot"] = Relationship(back_populates="subject")
