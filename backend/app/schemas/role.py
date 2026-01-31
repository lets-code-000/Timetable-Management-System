from pydantic import BaseModel

class RoleCreate(BaseModel):
    role_name: str
    
class RoleRead(BaseModel):
    id: int
    role_name: str

    class Config:
        from_attributes = True
    
class DeleteRoleResponse(BaseModel):
    message: str
    data: RoleRead | None = None
    
    
        