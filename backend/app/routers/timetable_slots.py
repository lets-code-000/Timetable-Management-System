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

router = APIRouter()


@router.post("/", response_model=TimetableSlotRead)
def create_timetable_slot(
    slot: TimetableSlotCreate,
    session: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    timetable = session.get(Timetable, slot.timetable_id)

    if not timetable or timetable.college_id != current_user.college_id:
        raise HTTPException(status_code=404, detail="Timetable not found")

    if slot.start_time >= slot.end_time:
        raise HTTPException(
            status_code=400,
            detail="Enter a valid time range where start_time is before end_time"
        )

    existing_slot = session.exec(
        select(TimetableSlot).where(
            TimetableSlot.classroom_id == slot.classroom_id,
            TimetableSlot.day_of_week == slot.day_of_week,
            TimetableSlot.start_time < slot.end_time,
            TimetableSlot.end_time > slot.start_time,
        )
    ).first()

    if existing_slot:
        raise HTTPException(
            status_code=400,
            detail="Classroom is already occupied during this time slot"
        )

    faculty_conflict = session.exec(
        select(TimetableSlot).where(
            TimetableSlot.faculty_id == slot.faculty_id,
            TimetableSlot.day_of_week == slot.day_of_week,
            TimetableSlot.start_time < slot.end_time,
            TimetableSlot.end_time > slot.start_time,
        )
    ).first()

    if faculty_conflict:
        raise HTTPException(
            status_code=400,
            detail="Faculty is already assigned to another class during this time"
        )

    # Create slot
    db_slot = TimetableSlot.model_validate(slot)

    session.add(db_slot)
    session.commit()
    session.refresh(db_slot)

    return db_slot


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

    if timetable.college_id != current_user.college_id:
        raise HTTPException(status_code=403, detail="Not authorized")

    return db_slot


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

    if timetable.college_id != current_user.college_id:
        raise HTTPException(status_code=403, detail="Not authorized")

    # Handle partial updates safely
    new_faculty_id = slot.faculty_id if slot.faculty_id is not None else db_slot.faculty_id
    new_day = slot.day_of_week if slot.day_of_week is not None else db_slot.day_of_week
    new_start = slot.start_time if slot.start_time is not None else db_slot.start_time
    new_end = slot.end_time if slot.end_time is not None else db_slot.end_time
    new_classroom_id = slot.classroom_id if slot.classroom_id is not None else db_slot.classroom_id

    # Time validation
    if new_start >= new_end:
        raise HTTPException(
            status_code=400,
            detail="Enter a valid time range where start_time is before end_time"
        )

    # Classroom conflict
    classroom_conflict = session.exec(
        select(TimetableSlot).where(
            TimetableSlot.classroom_id == new_classroom_id,
            TimetableSlot.day_of_week == new_day,
            TimetableSlot.start_time < new_end,
            TimetableSlot.end_time > new_start,
            TimetableSlot.id != slot_id,
        )
    ).first()

    if classroom_conflict:
        raise HTTPException(
            status_code=400,
            detail="Classroom is already occupied during this time slot"
        )

    # Faculty conflict
    faculty_conflict = session.exec(
        select(TimetableSlot).where(
            TimetableSlot.faculty_id == new_faculty_id,
            TimetableSlot.day_of_week == new_day,
            TimetableSlot.start_time < new_end,
            TimetableSlot.end_time > new_start,
            TimetableSlot.id != slot_id,
        )
    ).first()

    if faculty_conflict:
        raise HTTPException(
            status_code=400,
            detail="Faculty is already assigned to another class during this time"
        )

    # Apply updates
    slot_data = slot.model_dump(exclude_unset=True)
    for field, value in slot_data.items():
        setattr(db_slot, field, value)

    session.add(db_slot)
    session.commit()
    session.refresh(db_slot)

    return db_slot


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

    if timetable.college_id != current_user.college_id:
        raise HTTPException(status_code=403, detail="Not authorized")

    slot_public = TimetableSlotRead.model_validate(db_slot)

    session.delete(db_slot)
    session.commit()

    return DeleteTimetableSlotResponse(
        message="Timetable slot deleted successfully",
        data=slot_public
    )
