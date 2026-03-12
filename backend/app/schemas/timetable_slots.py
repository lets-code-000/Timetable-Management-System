from typing import Optional
from datetime import time, datetime
from sqlmodel import SQLModel
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
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class DeleteTimetableSlotResponse(SQLModel):
    message: str
    data: TimetableSlotRead | None = None