from typing import Optional
from sqlmodel import SQLModel
from datetime import datetime
from app.models.timetable import SemesterEnum
from app.schemas.department import DepartmentRead
from app.schemas.faculty import FacultyRead


class TimetableBase(SQLModel):
    department_id: int
    class_coordinator_id: int
    academic_year: str
    semester: SemesterEnum


class TimetableCreate(TimetableBase):
    pass


class TimetableUpdate(SQLModel):
    department_id: Optional[int] = None
    class_coordinator_id: Optional[int] = None
    academic_year: Optional[str] = None
    semester: Optional[SemesterEnum] = None


class TimetableRead(SQLModel):
    id: int
    college_id: Optional[int] = None
    department_id: int
    class_coordinator_id: int
    academic_year: str
    semester: SemesterEnum
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    department: Optional[DepartmentRead] = None
    class_coordinator: Optional[FacultyRead] = None

    class Config:
        from_attributes = True


class DeleteTimetableResponse(SQLModel):
    message: str
    data: TimetableRead | None = None
