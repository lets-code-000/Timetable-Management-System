from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List
from app.database import get_db
from app.models.subject import Subject
from app.models.faculty import Faculty
from app.models.department import Department
from app.schemas.subject import SubjectCreate, SubjectRead, SubjectUpdate, DeleteSubjectResponse
from app.schemas.utils import DeleteResponse
from app.crud.deps import get_current_user

router = APIRouter()

@router.post("/", response_model=SubjectRead)
def create_subject(subject: SubjectCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    if not db.get(Faculty, subject.faculty_id):
        raise HTTPException(status_code=404, detail="Faculty not found")
    if not db.get(Department, subject.department_id):
        raise HTTPException(status_code=404, detail="Department not found")
    db_subject = Subject.model_validate(subject)
    db_subject.college_id = current_user.college_id
    db.add(db_subject)
    db.commit()
    db.refresh(db_subject)
    return db_subject

@router.get("/", response_model=List[SubjectRead])
def get_subjects(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return db.exec(select(Subject).where(Subject.college_id == current_user.college_id)).all()

@router.get("/{subject_id}", response_model=SubjectRead)
def get_subject_by_id(subject_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    db_subject = db.get(Subject, subject_id)
    if not db_subject:
        raise HTTPException(status_code=404, detail="Subject not found")
    return db_subject

@router.put("/{subject_id}", response_model=SubjectRead)
def update_subject(subject_id: int, subject: SubjectUpdate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    db_subject = db.get(Subject, subject_id)
    if not db_subject:
        raise HTTPException(status_code=404, detail="Subject not found")
    if not db.get(Faculty, subject.faculty_id):
        raise HTTPException(status_code=404, detail="Faculty not found")
    if not db.get(Department, subject.department_id):
        raise HTTPException(status_code=404, detail="Department not found")
    subject_data = subject.model_dump(exclude_unset=True)
    for field, value in subject_data.items():
        setattr(db_subject, field, value)
    
    db.add(db_subject)
    db.commit()
    db.refresh(db_subject)
    return db_subject

@router.delete("/{subject_id}", response_model=DeleteSubjectResponse)
def delete_subject(subject_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    db_subject = db.get(Subject, subject_id)
    if not db_subject:
        raise HTTPException(status_code=404, detail="Subject not found")
    
    subject_public = SubjectRead.model_validate(db_subject)
    db.delete(db_subject)
    db.commit()
    return DeleteSubjectResponse(message="Subject deleted successfully",
                          data=subject_public
                        )


