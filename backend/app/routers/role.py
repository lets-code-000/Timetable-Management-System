from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, func, select
from app.database import get_db
from app.models.roles import Role
from app.schemas.role import RoleCreate, RoleRead, DeleteRoleResponse
from app.crud.deps import get_current_user

router = APIRouter()


@router.post("/", response_model=RoleRead)
def add_role(role: RoleCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    db_role = Role(role_name=role.role_name)
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    return db_role


@router.get("/", response_model=list[RoleRead])
def read_roles(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
    name: str | None = None,
):
    query = select(Role)

    if name:
        query = query.where(
            func.trim(func.lower(Role.role_name))
            .like(f"{name.strip().lower()}%")
        )

    roles = db.exec(query).all()
    return roles


@router.get("/{role_id}", response_model=RoleRead)
def read_role(role_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    role = db.get(Role, role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    return role


@router.delete("/{role_id}", response_model=DeleteRoleResponse)
def remove_role(role_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    role = db.get(Role, role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")

    role_public = RoleRead.model_validate(role)
    db.delete(role)
    db.commit()
    return DeleteRoleResponse(message="Role deleted successfully", data=role_public)
