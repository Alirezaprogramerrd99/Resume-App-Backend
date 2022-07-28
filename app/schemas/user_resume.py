from typing import List, Optional

from app.schemas.resume import InterdisciplinaryInteractionResumeCreate, \
    InternationalInteractionResumeCreate, ProjectResumeCreate,\
    NetworkResumeCreate, ExpertiseCreate , FieldOfStudyCreate ,\
    ManagementHistoryResumeCreate, OrganizationResumeCreate

from app.schemas.user import UserMain, GeneralInfo, GeneralID

from app.schemas.user import User
from pydantic import UUID4, BaseModel, EmailStr


# Shared properties
class UserResumeMain(BaseModel):
    international_interactions: List[InternationalInteractionResumeCreate]
    interdisciplinary_interactions: List[InterdisciplinaryInteractionResumeCreate]  # noqa
    projects: List[ProjectResumeCreate]
    networks: List[NetworkResumeCreate]
    management_histories: List[ManagementHistoryResumeCreate]
    organizations: List[OrganizationResumeCreate]
    expertises: List[ExpertiseCreate]
    field_of_studies: List[FieldOfStudyCreate]


class UserResumeBase(UserMain, GeneralInfo, GeneralID, UserResumeMain):
    # first_name: Optional[str] = None
    # last_name: Optional[str] = None
    # gender: Optional[str] = None
    # profile_image: Optional[str] = None
    # email: Optional[EmailStr] = None
    # phone_number: Optional[str] = None
    # field_of_study_id: Optional[UUID4]
    # grade_id: Optional[UUID4]
    # expertise_id: Optional[UUID4]
    # college_id: Optional[UUID4]
    # international_interactions: List[InternationalInteractionResumeCreate]
    # interdisciplinary_interactions: List[InterdisciplinaryInteractionResumeCreate]  # noqa
    # projects: List[ProjectResumeCreate]
    # networks: List[NetworkResumeCreate]
    # management_histories: List[ManagementHistoryResumeCreate]
    # organizations: List[OrganizationResumeCreate]
    pass


# Properties to receive via API on creation
class UserResumeCreate(UserResumeBase):
    pass


# Properties to receive via API on update
class UserResumeUpdate(UserResumeBase):
    pass


class UserResumeInDBBase(UserResumeMain):
    # international_interactions: List[InternationalInteractionResumeCreate]
    # interdisciplinary_interactions: List[InterdisciplinaryInteractionResumeCreate]  # noqa
    # projects: List[ProjectResumeCreate]
    # networks: List[NetworkResumeCreate]
    # management_histories: List[ManagementHistoryResumeCreate]
    # organizations: List[OrganizationResumeCreate]
    user: User

    class Config:
        orm_mode = True


# Additional properties to return via API
class UserResume(UserResumeInDBBase):
    pass


class UserResumeInDB(UserResumeInDBBase):
    pass
