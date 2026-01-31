from typing import Optional
from sqlmodel import SQLModel
from app.schemas.department import DepartmentRead

class FacultyBase(SQLModel):
    name: str
    department_id: int

class FacultyCreate(FacultyBase):
    pass

class FacultyUpdate(SQLModel):
    name: Optional[str] = None
    department_id: Optional[int] = None

class FacultyRead(SQLModel):
    id: int
    name: str
    college_id: Optional[int] = None
    department: Optional[DepartmentRead] = None

    class Config:
        from_attributes = True
        
class DeleteFacultyResponse(SQLModel):
    message: str
    data: FacultyRead | None = None


