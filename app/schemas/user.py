from datetime import datetime
from typing import List, Optional

from app.schemas.role import Role
from app.schemas.general_information import College,\
    Expertise, FieldOfStudy, Grade
from app.schemas.permission import Permission
from pydantic import UUID4, BaseModel, EmailStr
from app.schemas.pagination import  Pagination


# Shared properties
class UserMain(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None


class GeneralInfo(BaseModel):
    phone_number: Optional[str] = None
    profile_image: Optional[str] = None
    gender: Optional[str] = None


class GeneralID(BaseModel):
    grade_id: Optional[UUID4] = None
    field_of_study_id: Optional[UUID4] = None
    college_id: Optional[UUID4] = None
    expertise_id: Optional[UUID4] = None


class PermissionRoleIDBase(BaseModel):
    role_id: UUID4
    permissions: List[UUID4]


class DBTimeBase(BaseModel):
    id: UUID4
    role: Optional[Role]
    created_at: datetime
    updated_at: datetime


class PasswordBase(BaseModel):
    password: Optional[str] = None


class UserState(BaseModel):
    is_active: Optional[bool] = True


class PasswordOP(BaseModel):
    email: EmailStr

# ---------- Main types -------------------------

class UserBase(UserMain, GeneralInfo, UserState):
    # email: Optional[EmailStr] = None
    # is_active: Optional[bool] = True
    # phone_number: Optional[str] = None
    # first_name: Optional[str] = None
    # last_name: Optional[str] = None
    # profile_image: Optional[str] = None
    # gender: Optional[str] = None
    pass


class AdminGetMe(UserBase):
    profile_image_id: Optional[str] = None

# extends UserMain with password.
class UserRegister(UserMain, PasswordBase):
    # first_name: Optional[str] = None
    # last_name: Optional[str] = None
    # email: Optional[EmailStr] = None
    # password: Optional[str] = None
    pass


# Properties to receive via API on creation
class UserCreate(UserMain, GeneralInfo, GeneralID, PasswordBase, UserState):
    # email: Optional[EmailStr] = None
    # is_active: Optional[bool] = True
    # phone_number: Optional[str] = None
    # first_name: Optional[str] = None
    # last_name: Optional[str] = None
    # profile_image: Optional[str] = None
    # gender: Optional[str] = None
    # grade_id: Optional[UUID4] = None
    # field_of_study_id: Optional[UUID4] = None
    # college_id: Optional[UUID4] = None
    # expertise_id: Optional[UUID4] = None
    # password: Optional[str] = None
    pass


class AdminCreate(UserBase, PermissionRoleIDBase, PasswordBase):
    # password: Optional[str] = None
    # role_id: UUID4
    # permissions: List[UUID4]
    pass


class AdminUpdate(UserBase, PermissionRoleIDBase):
    new_password: Optional[str] = None
    # role_id: UUID4
    # permissions: List[UUID4]


class AdminUpdateMe(UserMain):
    # email: Optional[EmailStr] = None
    phone_number: Optional[str] = None
    # first_name: Optional[str] = None
    # last_name: Optional[str] = None
    profile_image: Optional[str] = None
    old_password: Optional[str] = None
    new_password: Optional[str] = None


class Admin(UserBase, DBTimeBase):
    # id: UUID4
    profile_image_id: Optional[str]
    # role: Optional[Role]
    # created_at: datetime
    # updated_at: datetime
    permissions: List[Permission]

    class Config:
        orm_mode = True

# Properties to receive via API on update


class AdminApiSchema(BaseModel):
    data: List[Admin]
    pagination: Pagination


class UserUpdate(UserMain, GeneralInfo, GeneralID, UserState):
    # email: Optional[EmailStr] = None
    # is_active: Optional[bool] = True
    # phone_number: Optional[str] = None
    # first_name: Optional[str] = None
    # last_name: Optional[str] = None
    # profile_image: Optional[str] = None
    # gender: Optional[str] = None
    # grade_id: Optional[UUID4] = None
    # field_of_study_id: Optional[UUID4] = None
    # college_id: Optional[UUID4] = None
    # expertise_id: Optional[UUID4] = None
    pass


class UserInDBBase(UserBase, DBTimeBase):
    # id: UUID4
    # role: Optional[Role]
    college: Optional[College]
    expertise: Optional[Expertise]
    field_of_study: Optional[FieldOfStudy]
    grade: Optional[Grade]

    # created_at: datetime
    # updated_at: datetime

    class Config:
        orm_mode = True


# Additional properties to return via API
class User(UserInDBBase):
    pass


class UserApiSchema(BaseModel):
    data: List[User]
    pagination: Pagination

    # Additional properties stored in DB


class UserInDB(UserInDBBase):
    hashed_password: str




class ForgetPassword(PasswordOP):
    pass




class ChangePassword(PasswordOP):
    code: str
    new_password: str
