from datetime import datetime, time
from sqlmodel import SQLModel, Field, Relationship

from app.schemas.utils import DayOfWeek


class TimetableSlot(SQLModel, table=True):
    __tablename__ = "timetable_slots"

    id: int | None = Field(default=None, primary_key=True)

    timetable_id: int = Field(foreign_key="timetable.id")
    classroom_id: int = Field(foreign_key="classroom.id")
    subject_id: int = Field(foreign_key="subject.id")
    faculty_id: int = Field(foreign_key="faculty.id")

    day_of_week: DayOfWeek
    start_time: time
    end_time: time

    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    timetable: "Timetable" = Relationship(back_populates="slots")
    classroom: "Classroom" = Relationship(back_populates="slots")
    subject: "Subject" = Relationship(back_populates="slots")
    faculty: "Faculty" = Relationship(back_populates="slots")