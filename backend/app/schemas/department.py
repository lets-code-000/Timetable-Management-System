from typing import Optional
from sqlmodel import SQLModel

class DepartmentBase(SQLModel):
    name: str
    year: int

class DepartmentCreate(DepartmentBase):
    pass

class DepartmentUpdate(SQLModel):
    name: Optional[str] = None
    year: Optional[int] = None

class DepartmentRead(SQLModel):
    id: int
    name: str
    year: int
    college_id: Optional[int] = None

    class Config:
        from_attributes = True
        
class DeleteDepartmentResponse(SQLModel):
    message: str
    data: DepartmentRead | None = None
