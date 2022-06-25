from app import models
from sqlalchemy.orm import Session


class CRUDDashboard:
    def get_users_count_based_on_gender(self, db: Session):
        male_count = db.query(models.User).filter(
            models.User.gender == "m").count()
        female_count = db.query(models.User).filter(
            models.User.gender == "f").count()
        return male_count, female_count

    def get_users_count_based_on_grade(self, db: Session, grade_id):
        count = db.query(models.User).filter(
            models.User.grade_id == grade_id).count()
        return count


dashboard = CRUDDashboard()
