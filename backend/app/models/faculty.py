from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship


class Faculty(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    department_id: int = Field(foreign_key="department.id")
    college_id: Optional[int] = Field(default=None, foreign_key="college.id")

    # Relationships
    department: "Department" = Relationship()
    college: "College" = Relationship(back_populates="faculties")
    subjects: list["Subject"] = Relationship()
