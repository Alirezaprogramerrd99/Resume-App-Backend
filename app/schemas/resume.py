
# from turtle import title
from typing import Optional

from pydantic import UUID4, BaseModel
from datetime import date
from .user import User

# region Project

class ProjectUserInfoInDBBase(BaseModel):
    id: UUID4
    user: User

class TitleBase(BaseModel):
    title: Optional[str]

class PositionBase(BaseModel):
    position: Optional[str]

class ProjectMain(TitleBase):
    employer: Optional[str]
    date: Optional[str]
    description: Optional[str]


class TitleIDBase(TitleBase):
    user_id: Optional[UUID4]


class PositionUserIDBase(PositionBase):
    # position: Optional[str]
    user_id: Optional[UUID4]

# ---------------- Main types ---------------------

class ProjectBase(ProjectMain):
    # title: Optional[str]
    # employer: Optional[str]
    # date: Optional[str]
    # description: Optional[str]
    user_id: Optional[UUID4]


class ProjectCreate(ProjectBase):
    date: Optional[date]


class ProjectUpdate(ProjectBase):
    pass


class ProjectInDBBase(ProjectBase, ProjectUserInfoInDBBase):
    # id: UUID4
    # user: User

    class Config:
        orm_mode = True


class Project(ProjectInDBBase):
    pass


class ProjectInDB(ProjectInDBBase):
    pass

# endregion


# region InterdisciplinaryInteraction


class InterdisciplinaryInteractionBase(TitleIDBase):
    # title: Optional[str]
    # user_id: Optional[UUID4]
    pass


# Properties to receive via API on creation
class InterdisciplinaryInteractionCreate(InterdisciplinaryInteractionBase):
    pass


# Properties to receive via API on update
class InterdisciplinaryInteractionUpdate(InterdisciplinaryInteractionBase):
    pass


class InterdisciplinaryInteractionInDBBase(InterdisciplinaryInteractionBase, ProjectUserInfoInDBBase):
    # id: UUID4
    # user: User

    class Config:
        orm_mode = True


class InterdisciplinaryInteraction(InterdisciplinaryInteractionInDBBase):
    pass


class InterdisciplinaryInteractionInDB(InterdisciplinaryInteractionInDBBase):
    pass

# endregion


# region Network


class NetworkBase(TitleIDBase):
    # title: Optional[str]
    # user_id: Optional[UUID4]
    pass


class NetworkCreate(NetworkBase):
    pass


class NetworkUpdate(NetworkBase):
    pass


class NetworkInDBBase(NetworkBase, ProjectUserInfoInDBBase):
    # id: UUID4
    # user: User

    class Config:
        orm_mode = True


class Network(NetworkInDBBase):
    pass


class NetworkInDB(NetworkInDBBase):
    pass

# endregion


# region InternationalInteraction


class InternationalInteractionBase(TitleIDBase):
    # title: Optional[str]
    # user_id: Optional[UUID4]
    pass


class InternationalInteractionCreate(InternationalInteractionBase):
    pass


class InternationalInteractionUpdate(InternationalInteractionBase):
    pass


class InternationalInteractionInDBBase(InternationalInteractionBase, ProjectUserInfoInDBBase):
    # id: UUID4
    # user: User

    class Config:
        orm_mode = True


class InternationalInteraction(InternationalInteractionInDBBase):
    pass


class InternationalInteractionInDB(InternationalInteractionInDBBase):
    pass

# endregion


# region ManagementHistory


class ManagementHistoryBase(PositionUserIDBase):
    # position: Optional[str]
    project_organization_name: Optional[str]
    # user_id: Optional[UUID4]


class ManagementHistoryCreate(ManagementHistoryBase):
    pass


class ManagementHistoryUpdate(ManagementHistoryBase):
    pass


class ManagementHistoryInDBBase(ManagementHistoryBase, ProjectUserInfoInDBBase):
    # id: UUID4
    # user: User

    class Config:
        orm_mode = True


class ManagementHistory(ManagementHistoryInDBBase):
    pass


class ManagementHistoryInDB(ManagementHistoryInDBBase):
    pass

# endregion


# region Organization


class OrganizationBase(PositionUserIDBase):
    # position: Optional[str]
    organization_name: Optional[str]
    # user_id: Optional[UUID4]


class OrganizationCreate(OrganizationBase):
    pass


class OrganizationUpdate(OrganizationBase):
    pass


class OrganizationInDBBase(OrganizationBase, ProjectUserInfoInDBBase):
    # id: UUID4
    # user: User

    class Config:
        orm_mode = True


class Organization(OrganizationInDBBase):
    pass


class OrganizationInDB(OrganizationInDBBase):
    pass

#----------------------------------------------------------
#------------------- FieldOfStudy -------------------------

class FieldOfStudyBase(TitleBase):
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


#------------------ Expertise---------------------------------
class ExpertiseBase(TitleBase):
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

# endregion

# ----------------------------------------
# ----------------------------------------
# ----------------------------------------

class ProjectResumeCreate(ProjectMain):
    # title: Optional[str]
    # employer: Optional[str]
    # date: Optional[str]
    # description: Optional[str]
    pass


class InterdisciplinaryInteractionResumeCreate(TitleBase):
    # title: Optional[str]
    pass


class NetworkResumeCreate(TitleBase):
    # title: Optional[str]
    pass


class InternationalInteractionResumeCreate(TitleBase):
    # title: Optional[str]
    pass


class ManagementHistoryResumeCreate(PositionBase):
    # position: Optional[str]
    project_organization_name: Optional[str]


class OrganizationResumeCreate(PositionBase):
    # position: Optional[str]
    organization_name: Optional[str]


class ExpertiseResumeCreate(TitleBase):
    pass

class FieldOfStudyResumeCreate(TitleBase):
    pass