from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List

router = APIRouter()

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
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    timetable = db.get(Timetable, slot.timetable_id)

    if not timetable or timetable.college_id != current_user.college_id:
        raise HTTPException(status_code=404, detail="Timetable not found")

    db_slot = TimetableSlot.model_validate(slot)

    db.add(db_slot)
    db.commit()
    db.refresh(db_slot)

    return db_slot

@router.get("/", response_model=List[TimetableSlotRead])
def get_timetable_slots(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    query = (
        select(TimetableSlot)
        .join(Timetable)
        .where(Timetable.college_id == current_user.college_id)
    )

    slots = db.exec(query).all()
    return slots

@router.get("/{slot_id}", response_model=TimetableSlotRead)
def get_timetable_slot_by_id(
    slot_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    slot = db.get(TimetableSlot, slot_id)

    if not slot:
        raise HTTPException(status_code=404, detail="Timetable slot not found")

    timetable = db.get(Timetable, slot.timetable_id)

    if timetable.college_id != current_user.college_id:
        raise HTTPException(status_code=403, detail="Not authorized")

    return slot

@router.put("/{slot_id}", response_model=TimetableSlotRead)
def update_timetable_slot(
    slot_id: int,
    slot: TimetableSlotUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    db_slot = db.get(TimetableSlot, slot_id)

    if not db_slot:
        raise HTTPException(status_code=404, detail="Timetable slot not found")

    timetable = db.get(Timetable, db_slot.timetable_id)

    if timetable.college_id != current_user.college_id:
        raise HTTPException(status_code=403, detail="Not authorized")

    slot_data = slot.model_dump(exclude_unset=True)

    for field, value in slot_data.items():
        setattr(db_slot, field, value)

    db.add(db_slot)
    db.commit()
    db.refresh(db_slot)

    return db_slot

@router.delete("/{slot_id}", response_model=DeleteTimetableSlotResponse)
def delete_timetable_slot(
    slot_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    db_slot = db.get(TimetableSlot, slot_id)

    if not db_slot:
        raise HTTPException(status_code=404, detail="Timetable slot not found")

    timetable = db.get(Timetable, db_slot.timetable_id)

    if timetable.college_id != current_user.college_id:
        raise HTTPException(status_code=403, detail="Not authorized")

    slot_public = TimetableSlotRead.model_validate(db_slot)

    db.delete(db_slot)
    db.commit()

    return DeleteTimetableSlotResponse(
        message="Timetable slot deleted successfully",
        data=slot_public,
    )
    
    