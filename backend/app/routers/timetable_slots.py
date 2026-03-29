from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List

from app.database import get_db
from app.models.timetable_slots import TimetableSlot
from app.models.timetable import Timetable
from app.schemas.timetable_slots import (
    TimetableSlotCreate,
    TimetableSlotRead,
    TimetableSlotUpdate,
    DeleteTimetableSlotResponse,
)
from app.crud.deps import get_current_user
from app.utils.slot_validation import (
    validate_slot_conflicts,
    validate_time_and_duplicates,
)

router = APIRouter()


# CREATE SLOT
@router.post("/", response_model=TimetableSlotRead)
def create_timetable_slot(
    slot: TimetableSlotCreate,
    session: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    timetable = session.get(Timetable, slot.timetable_id)

    if not timetable or timetable.college_id != current_user.college_id:
        raise HTTPException(status_code=404, detail="Timetable not found")

    # Time and Duplicate Validation
    validate_time_and_duplicates(
        session,
        timetable_id=slot.timetable_id,
        classroom_id=slot.classroom_id,
        faculty_id=slot.faculty_id,
        subject_id=slot.subject_id,
        day_of_week=slot.day_of_week,
        start_time=slot.start_time,
        end_time=slot.end_time,
    )

    # Conflict Validation
    validate_slot_conflicts(
        session,
        faculty_id=slot.faculty_id,
        classroom_id=slot.classroom_id,
        department_id=timetable.department_id,
        day_of_week=slot.day_of_week,
        start_time=slot.start_time,
        end_time=slot.end_time,
    )

    db_slot = TimetableSlot.model_validate(slot)

    session.add(db_slot)
    session.commit()
    session.refresh(db_slot)

    return db_slot


# GET ALL
@router.get("/", response_model=List[TimetableSlotRead])
def get_timetable_slots(
    session: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    query = (
        select(TimetableSlot)
        .join(Timetable)
        .where(Timetable.college_id == current_user.college_id)
    )

    return session.exec(query).all()


# GET BY ID 
@router.get("/{slot_id}", response_model=TimetableSlotRead)
def get_timetable_slot_by_id(
    slot_id: int,
    session: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    db_slot = session.get(TimetableSlot, slot_id)

    if not db_slot:
        raise HTTPException(status_code=404, detail="Timetable slot not found")

    timetable = session.get(Timetable, db_slot.timetable_id)

    if not timetable or timetable.college_id != current_user.college_id:
        raise HTTPException(status_code=403, detail="Not authorized")

    return db_slot


# UPDATE SLOT
@router.put("/{slot_id}", response_model=TimetableSlotRead)
def update_timetable_slot(
    slot_id: int,
    slot: TimetableSlotUpdate,
    session: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    db_slot = session.get(TimetableSlot, slot_id)

    if not db_slot:
        raise HTTPException(status_code=404, detail="Timetable slot not found")

    timetable = session.get(Timetable, db_slot.timetable_id)

    if not timetable or timetable.college_id != current_user.college_id:
        raise HTTPException(status_code=403, detail="Not authorized")

    # Time and Duplicate Validation
    validate_time_and_duplicates(
        session,
        timetable_id=slot.timetable_id,
        classroom_id=slot.classroom_id,
        faculty_id=slot.faculty_id,
        subject_id=slot.subject_id,
        day_of_week=slot.day_of_week,
        start_time=slot.start_time,
        end_time=slot.end_time,
        exclude_slot_id=slot_id,
    )

    # Conflict Validation
    validate_slot_conflicts(
        session,
        faculty_id=slot.faculty_id,
        classroom_id=slot.classroom_id,
        department_id=timetable.department_id,
        day_of_week=slot.day_of_week,
        start_time=slot.start_time,
        end_time=slot.end_time,
        exclude_slot_id=slot_id,
    )

    for field, value in slot.model_dump().items():
        setattr(db_slot, field, value)

    session.add(db_slot)
    session.commit()
    session.refresh(db_slot)

    return db_slot


# DELETE SLOT
@router.delete("/{slot_id}", response_model=DeleteTimetableSlotResponse)
def delete_timetable_slot(
    slot_id: int,
    session: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    db_slot = session.get(TimetableSlot, slot_id)

    if not db_slot:
        raise HTTPException(status_code=404, detail="Timetable slot not found")

    timetable = session.get(Timetable, db_slot.timetable_id)

    if not timetable or timetable.college_id != current_user.college_id:
        raise HTTPException(status_code=403, detail="Not authorized")

    slot_public = TimetableSlotRead.model_validate(db_slot)

    session.delete(db_slot)
    session.commit()

    return DeleteTimetableSlotResponse(
        message="Timetable slot deleted successfully",
        data=slot_public
    )
