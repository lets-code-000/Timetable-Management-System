from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship


class Faculty(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    department_id: int = Field(foreign_key="department.id")

    # Relationships
    department: "Department" = Relationship()
    subjects: list["Subject"] = Relationship()
