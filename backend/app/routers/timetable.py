from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List
from app.database import get_db
from app.models.timetable import Timetable
from app.models.department import Department
from app.models.faculty import Faculty
from app.schemas.timetable import (
    TimetableCreate,
    TimetableRead,
    TimetableUpdate,
    DeleteTimetableResponse,
)
from app.crud.deps import get_current_user
from sqlalchemy.exc import IntegrityError

router = APIRouter()


@router.post("/", response_model=TimetableRead)
def create_timetable(
    timetable: TimetableCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    # Validate department exists
    department = db.get(Department, timetable.department_id)
    if not department:
        raise HTTPException(status_code=404, detail="Department not found")

    # Validate class coordinator exists
    coordinator = db.get(Faculty, timetable.class_coordinator_id)
    if not coordinator:
        raise HTTPException(status_code=404, detail="Class coordinator not found")

    # Check unique constraint before inserting
    existing = db.exec(
        select(Timetable).where(
            Timetable.department_id == timetable.department_id,
            Timetable.academic_year == timetable.academic_year,
            Timetable.semester == timetable.semester,
        )
    ).first()
    if existing:
        raise HTTPException(
            status_code=400,
            detail="Timetable for this department, academic year and semester already exists",
        )

    # Create timetable with auto-assigned college_id
    db_timetable = Timetable.model_validate(timetable)
    db_timetable.college_id = current_user.college_id

    try:
        db.add(db_timetable)
        db.commit()
        db.refresh(db_timetable)
        return db_timetable
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Timetable for this department, academic year and semester already exists",
        )


@router.get("/", response_model=List[TimetableRead])
def get_timetables(
    db: Session = Depends(get_db), current_user=Depends(get_current_user)
):
    return db.exec(
        select(Timetable).where(Timetable.college_id == current_user.college_id)
    ).all()


@router.get("/{timetable_id}", response_model=TimetableRead)
def get_timetable_by_id(
    timetable_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    db_timetable = db.get(Timetable, timetable_id)
    if not db_timetable or db_timetable.college_id != current_user.college_id:
        raise HTTPException(status_code=404, detail="Timetable not found")

    return db_timetable


@router.put("/{timetable_id}", response_model=TimetableRead)
def update_timetable(
    timetable_id: int,
    timetable: TimetableUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    db_timetable = db.get(Timetable, timetable_id)
    if not db_timetable or db_timetable.college_id != current_user.college_id:
        raise HTTPException(status_code=404, detail="Timetable not found")

    timetable_data = timetable.model_dump(exclude_unset=True)

    # Validate department if being updated
    if "department_id" in timetable_data:
        department = db.get(Department, timetable_data["department_id"])
        if not department:
            raise HTTPException(status_code=404, detail="Department not found")

        # Check unique constraint for new department/year/semester combination
        new_dept_id = timetable_data.get("department_id", db_timetable.department_id)
        new_year = timetable_data.get("academic_year", db_timetable.academic_year)
        new_semester = timetable_data.get("semester", db_timetable.semester)

        existing = db.exec(
            select(Timetable).where(
                Timetable.department_id == new_dept_id,
                Timetable.academic_year == new_year,
                Timetable.semester == new_semester,
                Timetable.id != timetable_id,
            )
        ).first()
        if existing:
            raise HTTPException(
                status_code=400,
                detail="Timetable for this department, academic year and semester already exists",
            )

    # Validate coordinator if being updated
    if "class_coordinator_id" in timetable_data:
        coordinator = db.get(Faculty, timetable_data["class_coordinator_id"])
        if not coordinator:
            raise HTTPException(status_code=404, detail="Class coordinator not found")

    # Apply updates
    for field, value in timetable_data.items():
        setattr(db_timetable, field, value)

    try:
        db.add(db_timetable)
        db.commit()
        db.refresh(db_timetable)
        return db_timetable
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Timetable for this department, academic year and semester already exists",
        )


@router.delete("/{timetable_id}", response_model=DeleteTimetableResponse)
def delete_timetable(
    timetable_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    db_timetable = db.get(Timetable, timetable_id)
    if not db_timetable or db_timetable.college_id != current_user.college_id:
        raise HTTPException(status_code=404, detail="Timetable not found")

    timetable_public = TimetableRead.model_validate(db_timetable)
    db.delete(db_timetable)
    db.commit()

    return DeleteTimetableResponse(
        message="Timetable deleted successfully", data=timetable_public
    )
