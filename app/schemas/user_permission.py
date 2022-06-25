from typing import Optional

from app.schemas.permission import Permission
from pydantic import UUID4, BaseModel


# Shared properties
class UserPermissionBase(BaseModel):
    user_id: Optional[UUID4]
    permission_id: Optional[UUID4]


# Properties to receive via API on creation
class UserPermissionCreate(UserPermissionBase):
    pass


# Properties to receive via API on update
class UserPermissionUpdate(BaseModel):
    permission_id: UUID4


class UserPermissionInDBBase(UserPermissionBase):
    permission: Permission

    class Config:
        orm_mode = True


# Additional properties to return via API
class UserPermission(UserPermissionInDBBase):
    pass


class UserPermissionInDB(UserPermissionInDBBase):
    pass
