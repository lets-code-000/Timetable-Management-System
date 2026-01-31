from typing import Optional
from sqlmodel import SQLModel
from app.schemas.department import DepartmentRead

class ClassroomBase(SQLModel):
    building_name: str
    room_no: str
    capacity: int
    department_id: int

class ClassroomCreate(ClassroomBase):
    pass

class ClassroomUpdate(SQLModel):
    building_name: Optional[str] = None
    room_no: Optional[str] = None
    capacity: Optional[int] = None
    department_id: Optional[int] = None

class ClassroomRead(SQLModel):
    id: int
    building_name: str
    room_no: str
    capacity: int
    college_id: Optional[int] = None
    department: Optional[DepartmentRead] = None

    class Config:
        from_attributes = True

class DeleteClassroomResponse(SQLModel):
    message: str
    data: ClassroomRead| None = None