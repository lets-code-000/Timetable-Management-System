from fastapi import HTTPException
from sqlmodel import Session, select
from datetime import time

from app.models.timetable_slots import TimetableSlot
from app.models.timetable import Timetable
from app.schemas.utils import DayOfWeek


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
            detail="Start time must be before end time"
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

    duplicate_slot = session.exec(duplicate_query).first()

    if duplicate_slot:
        raise HTTPException(
            status_code=409,
            detail=(
                f"This exact slot already exists for "
                f"{duplicate_slot.subject.name} with "
                f"{duplicate_slot.faculty.name} in Room "
                f"{duplicate_slot.classroom.room_no} "
                f"from {duplicate_slot.start_time.strftime('%H:%M')} "
                f"to {duplicate_slot.end_time.strftime('%H:%M')} "
                f"({day_of_week})"
            )
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

    
    # 1. Classroom Conflict
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

    classroom_conflict = session.exec(classroom_query).first()

    if classroom_conflict:
        raise HTTPException(
            status_code=409,
            detail=(
                f"Room {classroom_conflict.classroom.room_no} "
                f"is already occupied by {classroom_conflict.subject.name} "
                f"handled by {classroom_conflict.faculty.name} "
                f"from {classroom_conflict.start_time.strftime('%H:%M')} "
                f"to {classroom_conflict.end_time.strftime('%H:%M')} "
                f"on {day_of_week}"
            )
        )

    # 2. Faculty Conflict
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

    faculty_conflict = session.exec(faculty_query).first()

    if faculty_conflict:
        raise HTTPException(
            status_code=409,
            detail=(
                f"{faculty_conflict.faculty.name} is already assigned to "
                f"{faculty_conflict.subject.name} in Room "
                f"{faculty_conflict.classroom.room_no} "
                f"from {faculty_conflict.start_time.strftime('%H:%M')} "
                f"to {faculty_conflict.end_time.strftime('%H:%M')} "
                f"on {day_of_week}"
            )
        )

    # 3. Department Conflict
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

    department_conflict = session.exec(department_query).first()

    if department_conflict:
        raise HTTPException(
            status_code=409,
            detail=(
                f"Department already has {department_conflict.subject.name} "
                f"in Room {department_conflict.classroom.room_no} "
                f"handled by {department_conflict.faculty.name} "
                f"from {department_conflict.start_time.strftime('%H:%M')} "
                f"to {department_conflict.end_time.strftime('%H:%M')} "
                f"on {day_of_week}"
            )
        )
        