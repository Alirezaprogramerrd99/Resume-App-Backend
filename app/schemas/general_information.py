from typing import List, Optional

from pydantic import UUID4, BaseModel

from app.schemas.pagination import Pagination


class GeneralFieldBase(BaseModel):
    name: Optional[str]
    description: Optional[str]


# Shared properties
class GradeBase(GeneralFieldBase):
    # name: Optional[str]
    # description: Optional[str]
    pass


# Properties to receive via API on creation
class GradeCreate(GradeBase):
    pass


# Properties to receive via API on update
class GradeUpdate(GradeBase):
    pass


class GradeInDBBase(GradeBase):
    id: UUID4

    class Config:
        orm_mode = True


# Additional properties to return via API
class Grade(GradeInDBBase):
    pass


class GradeInDB(GradeInDBBase):
    pass


# Shared properties
class CollegeBase(GeneralFieldBase):
    # name: Optional[str]
    # description: Optional[str]
    pass


# Properties to receive via API on creation
class CollegeCreate(CollegeBase):
    pass


# Properties to receive via API on update
class CollegeUpdate(CollegeBase):
    pass


class CollegeInDBBase(CollegeBase):
    id: UUID4

    class Config:
        orm_mode = True


# Additional properties to return via API
class College(CollegeInDBBase):
    pass


class CollegeInDB(CollegeInDBBase):
    pass


class GradeApiSchema(BaseModel):
    data: List[Grade]
    pagination: Pagination


class CollegeApiSchema(BaseModel):
    data: List[College]
    pagination: Pagination
