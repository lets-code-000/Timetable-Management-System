from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.database import get_db
from app.models.classroom import Classroom
from app.models.department import Department
from app.schemas.classroom import ClassroomCreate, ClassroomRead, ClassroomUpdate,DeleteClassroomResponse
from app.schemas.utils import DeleteResponse
from app.crud.deps import get_current_user

router = APIRouter()

@router.post("/", response_model=ClassroomRead)
def create_classroom(classroom: ClassroomCreate, session: Session = Depends(get_db),current_user = Depends(get_current_user)):
    # Check if department exists
    department = session.get(Department, classroom.department_id)
    if not department:
        raise HTTPException(status_code=404, detail="Department not found")

    db_classroom = Classroom.model_validate(classroom)
    db_classroom.college_id = current_user.college_id
    session.add(db_classroom)
    session.commit()
    session.refresh(db_classroom)
    return db_classroom

@router.get("/", response_model=list[ClassroomRead])
def get_classrooms(session: Session = Depends(get_db),current_user = Depends(get_current_user)):
    statement = select(Classroom).where(Classroom.college_id == current_user.college_id)
    results = session.exec(statement).all()
    return results

@router.get("/{classroom_id}", response_model=ClassroomRead)
def get_classroom_by_id(classroom_id: int, session: Session = Depends(get_db), current_user = Depends(get_current_user)):
    db_classroom = session.get(Classroom, classroom_id)
    if not db_classroom:
        raise HTTPException(status_code=404, detail="Classroom not found")
    return db_classroom

@router.put("/{classroom_id}", response_model=ClassroomRead)
def update_classroom(classroom_id: int, classroom: ClassroomUpdate, session: Session = Depends(get_db), current_user = Depends(get_current_user)):
    db_classroom = session.get(Classroom, classroom_id)
    if not db_classroom:
        raise HTTPException(status_code=404, detail="Classroom not found")
    classroom_data = classroom.model_dump(exclude_unset=True)
    
    # Ensure department exists if changed
    if "department_id" in classroom_data:
        department = session.get(Department, classroom_data["department_id"])
        if not department:
            raise HTTPException(status_code=404, detail="Department not found")
    
    for field, value in classroom_data.items():
        setattr(db_classroom, field, value)
    session.add(db_classroom)
    session.commit()
    session.refresh(db_classroom)
    return db_classroom
@router.delete("/{classroom_id}", response_model=DeleteClassroomResponse)
def delete_classroom(
    classroom_id: int,
    session: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    db_classroom = session.get(Classroom, classroom_id)
    if not db_classroom:
        raise HTTPException(status_code=404, detail="Classroom not found")

    
    classroom_public = ClassroomRead.model_validate(db_classroom)

    session.delete(db_classroom)
    session.commit()

    return DeleteClassroomResponse(
        message="Classroom deleted successfully",
        data=classroom_public
    )
