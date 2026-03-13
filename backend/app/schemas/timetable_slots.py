from typing import Optional
from datetime import datetime, time
from sqlmodel import SQLModel


from app.schemas.timetable import TimetableRead
from app.schemas.classroom import ClassroomRead
from app.schemas.subject import SubjectRead
from app.schemas.faculty import FacultyRead
from app.models.timetable_slots import DayOfWeek



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


class TimetableSlotUpdate(TimetableSlotBase):
    pass


class TimetableSlotRead(SQLModel):
    id: int
    timetable_id: int

    day_of_week: DayOfWeek
    start_time: time
    end_time: time
    created_at: Optional[datetime]

    subject: Optional[SubjectRead] = None
    faculty: Optional[FacultyRead] = None
    classroom: Optional[ClassroomRead] = None
    timetable: Optional[TimetableRead] = None

    class Config:
        from_attributes = True


class DeleteTimetableSlotResponse(SQLModel):
    message: str
    data: TimetableSlotRead | None = None
