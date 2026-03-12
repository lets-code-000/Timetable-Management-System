from typing import Optional
from enum import Enum
from datetime import datetime, time
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, DateTime, func


class DayOfWeek(str, Enum):
    MONDAY = "MONDAY"
    TUESDAY = "TUESDAY"
    WEDNESDAY = "WEDNESDAY"
    THURSDAY = "THURSDAY"
    FRIDAY = "FRIDAY"
    SATURDAY = "SATURDAY"


class TimetableSlot(SQLModel, table=True):
    __tablename__ = "timetable_slots"

    id: Optional[int] = Field(default=None, primary_key=True)

    timetable_id: int = Field(foreign_key="timetable.id")
    classroom_id: int = Field(foreign_key="classroom.id")
    subject_id: int = Field(foreign_key="subject.id")
    faculty_id: int = Field(foreign_key="faculty.id")

    day_of_week: DayOfWeek = Field()
    start_time: time
    end_time: time

    created_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True), server_default=func.now())
    )

    # Relationships
    timetable: "Timetable" = Relationship(back_populates="slots")
    classroom: "Classroom" = Relationship(back_populates="slots")
    subject: "Subject" = Relationship(back_populates="slots")
    faculty: "Faculty" = Relationship(back_populates="slots")