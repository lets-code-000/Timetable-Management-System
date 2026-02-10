from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, func, select
from typing import List
from app.database import get_db
from app.models.college import College
from app.schemas.college import CollegeCreate, CollegeRead, CollegeUpdate, DeleteCollegeResponse
from app.crud.deps import get_current_user

router = APIRouter()


@router.post("/", response_model=CollegeRead)
def create_college(college: CollegeCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    existing = db.exec(select(College).where(College.name == college.name)).first()
    if existing:
        raise HTTPException(status_code=400, detail="College with this name already exists")

    db_college = College.model_validate(college)
    db.add(db_college)
    db.commit()
    db.refresh(db_college)
    return db_college


@router.get("/", response_model=List[CollegeRead])
def get_colleges(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
    name: str | None = None,
):
    query = select(College)

    if name:
        query = query.where(
            func.trim(func.lower(College.name))
            .like(f"{name.strip().lower()}%")
        )

    colleges = db.exec(query).all()
    return colleges


@router.get("/public", response_model=List[CollegeRead])
def get_colleges_public(db: Session = Depends(get_db)):
    """Public endpoint for registration dropdown — no auth required."""
    colleges = db.exec(select(College)).all()
    return colleges


@router.get("/{college_id}", response_model=CollegeRead)
def get_college_by_id(college_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    college = db.get(College, college_id)
    if not college:
        raise HTTPException(status_code=404, detail="College not found")
    return college


@router.put("/{college_id}", response_model=CollegeRead)
def update_college(college_id: int, college: CollegeUpdate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    existing = db.get(College, college_id)
    if not existing:
        raise HTTPException(status_code=404, detail="College not found")

    college_data = college.model_dump(exclude_unset=True)
    for field, value in college_data.items():
        setattr(existing, field, value)

    db.add(existing)
    db.commit()
    db.refresh(existing)
    return existing


@router.delete("/{college_id}", response_model=DeleteCollegeResponse)
def delete_college(college_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    existing = db.get(College, college_id)
    if not existing:
        raise HTTPException(status_code=404, detail="College not found")

    college_public = CollegeRead.model_validate(existing)
    db.delete(existing)
    db.commit()
    return DeleteCollegeResponse(message="College deleted successfully", data=college_public)
