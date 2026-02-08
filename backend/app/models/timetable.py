from typing import Optional
from enum import IntEnum
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from sqlalchemy import Column, DateTime, UniqueConstraint, func


class SemesterEnum(IntEnum):
    SEMESTER_1 = 1
    SEMESTER_2 = 2
    SEMESTER_3 = 3
    SEMESTER_4 = 4
    SEMESTER_5 = 5
    SEMESTER_6 = 6
    SEMESTER_7 = 7
    SEMESTER_8 = 8


class Timetable(SQLModel, table=True):
    __tablename__ = "timetable"
    __table_args__ = (
        UniqueConstraint('department_id', 'academic_year', 'semester', name='uq_department_academic_year_semester'),
    )

    id: Optional[int] = Field(default=None, primary_key=True)
    college_id: Optional[int] = Field(default=None, foreign_key="college.id")
    department_id: int = Field(foreign_key="department.id")
    class_coordinator_id: int = Field(foreign_key="faculty.id")
    academic_year: str
    semester: SemesterEnum = Field()
    created_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True), server_default=func.now())
    )
    updated_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    )

    # Relationships
    college: "College" = Relationship(back_populates="timetables")
    department: "Department" = Relationship(back_populates="timetables")
    class_coordinator: "Faculty" = Relationship(back_populates="timetables")
