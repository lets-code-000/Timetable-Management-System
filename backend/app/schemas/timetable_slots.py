from typing import Optional
from datetime import datetime, time
from sqlmodel import SQLModel
from app.models.timetable_slots import DayOfWeek

from app.schemas.subject import SubjectRead
from app.schemas.faculty import FacultyRead
from app.schemas.classroom import ClassroomRead


class TimetableSlotBase(SQLModel):
    timetable_id: int
    classroom_id: int
    subject_id: int
    faculty_id: int
    day_of_week: DayOfWeek
    start_time: time
    end_time: time


class TimetableSlotCreate(TimetableSlotBase):
    pass


class TimetableSlotUpdate(SQLModel):
    timetable_id: Optional[int] = None
    classroom_id: Optional[int] = None
    subject_id: Optional[int] = None
    faculty_id: Optional[int] = None
    day_of_week: Optional[DayOfWeek] = None
    start_time: Optional[time] = None
    end_time: Optional[time] = None


class TimetableSlotRead(SQLModel):
    id: int
    timetable_id: int
    classroom_id: int
    subject_id: int
    faculty_id: int

    day_of_week: DayOfWeek
    start_time: time
    end_time: time
    created_at: Optional[datetime]

    # nested objects
    subject: Optional[SubjectRead] = None
    faculty: Optional[FacultyRead] = None
    classroom: Optional[ClassroomRead] = None

    class Config:
        from_attributes = True


class DeleteTimetableSlotResponse(SQLModel):
    message: str
    data: TimetableSlotRead | None = None