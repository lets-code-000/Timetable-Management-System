from fastapi import HTTPException
from sqlmodel import Session, select
from datetime import time

from app.models.timetable_slots import TimetableSlot
from app.schemas.utils import DayOfWeek


def validate_slot_conflicts(
    session: Session,
    *,
    faculty_id: int,
    classroom_id: int,
    day_of_week: DayOfWeek,
    start_time: time,
    end_time: time,
    exclude_slot_id: int | None = None,
):
    # Classroom Conflict
    classroom_query = select(TimetableSlot).where(
        TimetableSlot.classroom_id == classroom_id,
        TimetableSlot.day_of_week == day_of_week,
        TimetableSlot.start_time < end_time,
        TimetableSlot.end_time > start_time,
    )

    if exclude_slot_id is not None:
        classroom_query = classroom_query.where(
            TimetableSlot.id != exclude_slot_id
        )

    if session.exec(classroom_query).first():
        raise HTTPException(
            status_code=400,
            detail="Classroom is already occupied during this time slot"
        )

    # Faculty Conflict 
    faculty_query = select(TimetableSlot).where(
        TimetableSlot.faculty_id == faculty_id,
        TimetableSlot.day_of_week == day_of_week,
        TimetableSlot.start_time < end_time,
        TimetableSlot.end_time > start_time,
    )

    if exclude_slot_id is not None:
        faculty_query = faculty_query.where(
            TimetableSlot.id != exclude_slot_id
        )

    if session.exec(faculty_query).first():
        raise HTTPException(
            status_code=400,
            detail="Faculty is already assigned to another class during this time"
        )
        