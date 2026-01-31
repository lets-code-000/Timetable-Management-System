from typing import Optional
from sqlmodel import SQLModel
from app.schemas.department import DepartmentRead
from app.schemas.faculty import FacultyRead

class SubjectBase(SQLModel):
    name: str
    faculty_id: int
    department_id: int

class SubjectCreate(SubjectBase):
    pass

class SubjectUpdate(SQLModel):
    name: Optional[str] = None
    faculty_id: Optional[int] = None
    department_id: Optional[int] = None

class SubjectRead(SQLModel):
    id: int
    name: str
    college_id: Optional[int] = None
    faculty: Optional[FacultyRead] = None
    department: Optional[DepartmentRead] = None
    
class DeleteSubjectResponse(SQLModel):
    message: str
    data: SubjectRead | None = None

    class Config:
        from_attributes = True
        

