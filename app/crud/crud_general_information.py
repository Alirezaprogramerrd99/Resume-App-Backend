from typing import Optional

from app.crud.base import CRUDBase
from app.models import College, Expertise, FieldOfStudy, Grade
from app.schemas import CollegeCreate, CollegeUpdate,\
    ExpertiseCreate, ExpertiseUpdate, FieldOfStudyCreate, \
    FieldOfStudyUpdate, GradeCreate, GradeUpdate   # these ...create and ...updates are childs of baseModel
from sqlalchemy.orm import Session


class CRUDFieldOfStudy(
    CRUDBase[FieldOfStudy, FieldOfStudyCreate, FieldOfStudyUpdate]
):
    def get_by_name(self, db: Session, *, name: str):
        return db.query(self.model).filter(self.model.name == name).first()


class CRUDGrade(CRUDBase[Grade, GradeCreate, GradeUpdate]):
    def get_by_name(self, db: Session, *, name: str):
        return db.query(self.model).filter(self.model.name == name).first()


class CRUDCollege(CRUDBase[College, CollegeCreate, CollegeUpdate]):
    def get_by_name(self, db: Session, *, name: str):
        return db.query(self.model).filter(self.model.name == name).first()


class CRUDExpertise(CRUDBase[Expertise, ExpertiseCreate, ExpertiseUpdate]):
    def get_by_name(self, db: Session, *, name: str):
        return db.query(self.model).filter(self.model.name == name).first()

# FieldOfStudy, Grade, College, Expertise are sqlalchemy models(ORM) (not schema)
field_of_study = CRUDFieldOfStudy(FieldOfStudy)
grade = CRUDGrade(Grade)
college = CRUDCollege(College)
expertise = CRUDExpertise(Expertise)
