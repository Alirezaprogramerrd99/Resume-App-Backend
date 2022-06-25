
from pydantic import BaseModel


class UserGender(BaseModel):
    female_count: int
    male_count: int


class UserGrade(BaseModel):
    name: str
    count: int


class DashboardUserRegisterIn(BaseModel):
    year: int
    month : int
    chart_type: str 