from fastapi import HTTPException
from sqlmodel import Session, select
from datetime import time

from app.models.timetable_slots import TimetableSlot
from app.models.timetable import Timetable
from app.schemas.utils import DayOfWeek


# Time and Duplicate Validation 
def validate_time_and_duplicates(
    session: Session,
    *,
    timetable_id: int,
    classroom_id: int,
    faculty_id: int,
    subject_id: int,
    day_of_week: DayOfWeek,
    start_time: time,
    end_time: time,
    exclude_slot_id: int | None = None,
):
    # Time validation
    if start_time >= end_time:
        raise HTTPException(
            status_code=400,
            detail="start_time must be before end_time"
        )

    # Duplicate check
    duplicate_query = select(TimetableSlot).where(
        TimetableSlot.timetable_id == timetable_id,
        TimetableSlot.classroom_id == classroom_id,
        TimetableSlot.faculty_id == faculty_id,
        TimetableSlot.subject_id == subject_id,
        TimetableSlot.day_of_week == day_of_week,
        TimetableSlot.start_time == start_time,
        TimetableSlot.end_time == end_time,
    )

    if exclude_slot_id is not None:
        duplicate_query = duplicate_query.where(
            TimetableSlot.id != exclude_slot_id
        )

    if session.exec(duplicate_query).first():
        raise HTTPException(
            status_code=400,
            detail="Exact duplicate timetable slot already exists"
        )


# Conflict Validation 
def validate_slot_conflicts(
    session: Session,
    *,
    faculty_id: int,
    classroom_id: int,
    department_id: int,
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

    # Department Conflict
    department_query = select(TimetableSlot).join(
        Timetable, Timetable.id == TimetableSlot.timetable_id
    ).where(
        Timetable.department_id == department_id,
        TimetableSlot.day_of_week == day_of_week,
        TimetableSlot.start_time < end_time,
        TimetableSlot.end_time > start_time,
    )

    if exclude_slot_id is not None:
        department_query = department_query.where(
            TimetableSlot.id != exclude_slot_id
        )

    if session.exec(department_query).first():
        raise HTTPException(
            status_code=400,
            detail="Department already has a class during this time"
        )
