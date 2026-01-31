from sqlmodel import SQLModel


class DashboardReadStats(SQLModel):
    total_subjects: int
    total_faculties: int
    total_classrooms: int
    total_departments: int
