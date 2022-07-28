from typing import Optional

from app.crud.base import CRUDBase
from app.models import College, Grade
from app.schemas import CollegeCreate, CollegeUpdate,\
    GradeCreate, GradeUpdate   # these ...create and ...updates are childs of baseModel
from sqlalchemy.orm import Session


class CRUDGrade(CRUDBase[Grade, GradeCreate, GradeUpdate]):
    def get_by_name(self, db: Session, *, name: str):
        return db.query(self.model).filter(self.model.name == name).first()


class CRUDCollege(CRUDBase[College, CollegeCreate, CollegeUpdate]):
    def get_by_name(self, db: Session, *, name: str):
        return db.query(self.model).filter(self.model.name == name).first()


grade = CRUDGrade(Grade)
college = CRUDCollege(College)
