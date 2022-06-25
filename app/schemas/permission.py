from typing import Optional

from pydantic import UUID4, BaseModel

from app.schemas.role import PermissionRoleGeneralBase

# Shared properties
class PermissionBase(PermissionRoleGeneralBase):
    # name: Optional[str]
    # description: Optional[str]
    # persian_name: Optional[str]
    pass


# Properties to receive via API on creation
class PermissionCreate(PermissionBase):
    pass


# Properties to receive via API on update
class PermissionUpdate(PermissionBase):
    pass


class PermissionInDBBase(PermissionBase):
    id: UUID4

    class Config:
        orm_mode = True


# Additional properties to return via API
class Permission(PermissionInDBBase):
    pass


class PermissionInDB(PermissionInDBBase):
    pass
