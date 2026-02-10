from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, func, select
from typing import List
from app.database import get_db
from app.models.faculty import Faculty
from app.models.department import Department
from app.schemas.faculty import FacultyCreate, FacultyRead, FacultyUpdate, DeleteFacultyResponse
from app.schemas.utils import DeleteResponse
from app.crud.deps import get_current_user

router = APIRouter()

@router.post("/", response_model=FacultyRead)
def create_faculty(faculty: FacultyCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    if not db.get(Department, faculty.department_id):
        raise HTTPException(status_code=404, detail="Department not found")
    db_faculty = Faculty.model_validate(faculty)
    db_faculty.college_id = current_user.college_id
    db.add(db_faculty)
    db.commit()
    db.refresh(db_faculty)
    return db_faculty

@router.get("/", response_model=List[FacultyRead])
def get_faculties(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
    name: str | None = None,
):
    query = select(Faculty).where(
        Faculty.college_id == current_user.college_id
    )

    if name:
        query = query.where(
            func.trim(func.lower(Faculty.name))
            .like(f"{name.strip().lower()}%")
        )

    faculties = db.exec(query).all()
    return faculties

@router.get("/{faculty_id}", response_model=FacultyRead)
def get_faculty_by_id(faculty_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    db_faculty = db.get(Faculty, faculty_id)
    if not db_faculty:
        raise HTTPException(status_code=404, detail="Faculty not found")
    return db_faculty

@router.put("/{faculty_id}", response_model=FacultyRead)
def update_faculty(faculty_id: int, faculty: FacultyUpdate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    db_faculty = db.get(Faculty, faculty_id)
    if not db_faculty:
        raise HTTPException(status_code=404, detail="Faculty not found")
    if not db.get(Department, faculty.department_id):
        raise HTTPException(status_code=404, detail="Department not found")
    faculty_data = faculty.model_dump(exclude_unset=True)
    for field, value in faculty_data.items():
        setattr(db_faculty, field, value)
    
    db.add(db_faculty)
    db.commit()
    db.refresh(db_faculty)
    return db_faculty

@router.delete("/{faculty_id}", response_model=DeleteFacultyResponse)
def delete_faculty(faculty_id: int, db: Session = Depends(get_db), _current_user = Depends(get_current_user)): # noqa: B008
    db_faculty = db.get(Faculty, faculty_id)
    if not db_faculty:
        raise HTTPException(status_code=404, detail="Faculty not found")
    
    faculty_public = FacultyRead.model_validate(db_faculty)
    db.delete(db_faculty)
    db.commit()
    return DeleteFacultyResponse(message="Faculty deleted successfully",
                          data= faculty_public
                    )


