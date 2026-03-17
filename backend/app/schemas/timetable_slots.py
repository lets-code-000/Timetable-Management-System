from datetime import datetime, time
from sqlmodel import SQLModel


from app.schemas.timetable import TimetableRead
from app.schemas.classroom import ClassroomRead
from app.schemas.subject import SubjectRead
from app.schemas.faculty import FacultyRead
from app.schemas.utils import DayOfWeek



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


class TimetableSlotRead(TimetableSlotBase):
    id: int
    created_at: datetime | None

    subject: SubjectRead | None = None
    faculty: FacultyRead | None = None
    classroom: ClassroomRead | None = None
    timetable: TimetableRead | None = None

    class Config:
        from_attributes = True


class DeleteTimetableSlotResponse(SQLModel):
    message: str
    data: TimetableSlotRead | None = None
