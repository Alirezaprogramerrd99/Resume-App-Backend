from typing import List, Optional

from pydantic import UUID4, BaseModel

from app.schemas.pagination import Pagination

class GeneralFieldBase(BaseModel):
    name: Optional[str]
    description: Optional[str]


# Shared properties
class FieldOfStudyBase(GeneralFieldBase):
    # name: Optional[str]
    # description: Optional[str]
    pass


# Properties to receive via API on creation
class FieldOfStudyCreate(FieldOfStudyBase):
    pass


# Properties to receive via API on update
class FieldOfStudyUpdate(FieldOfStudyBase):
    pass


class FieldOfStudyInDBBase(FieldOfStudyBase):
    id: UUID4

    class Config:
        orm_mode = True


# Additional properties to return via API
class FieldOfStudy(FieldOfStudyInDBBase):
    pass


class FieldOfStudyInDB(FieldOfStudyInDBBase):
    pass


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


# Shared properties
class ExpertiseBase(GeneralFieldBase):
    # name: Optional[str]
    # description: Optional[str]
    pass


# Properties to receive via API on creation
class ExpertiseCreate(ExpertiseBase):
    pass


# Properties to receive via API on update
class ExpertiseUpdate(ExpertiseBase):
    pass


class ExpertiseInDBBase(ExpertiseBase):
    id: UUID4

    class Config:
        orm_mode = True


# Additional properties to return via API
class Expertise(ExpertiseInDBBase):
    pass


class ExpertiseInDB(ExpertiseInDBBase):
    pass


class FieldOfStudyApiSchema(BaseModel):
    data: List[FieldOfStudy]
    pagination : Pagination

class GradeApiSchema(BaseModel):
    data: List[Grade]
    pagination : Pagination

class ExpertiseApiSchema(BaseModel):
    data: List[Expertise]
    pagination : Pagination

class CollegeApiSchema(BaseModel):
    data: List[College]
    pagination : Pagination