from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List

class Classroom(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    building_name: str
    room_no: str
    capacity: int
    department_id: int = Field(foreign_key="department.id")
    college_id: Optional[int] = Field(default=None, foreign_key="college.id")

    department: "Department" = Relationship(back_populates="classrooms")
    college: "College" = Relationship(back_populates="classrooms")
    slots: List["TimetableSlot"] = Relationship(back_populates="classroom")
    