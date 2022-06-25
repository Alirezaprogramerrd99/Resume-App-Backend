from app.crud.base import CRUDBase
from app.models import Project, InterdisciplinaryInteraction, \
    Network, InternationalInteraction, ManagementHistory, Organization
from app.schemas import ProjectCreate, ProjectUpdate,\
    InterdisciplinaryInteractionCreate, InterdisciplinaryInteractionUpdate,\
    NetworkCreate, NetworkUpdate,\
    InternationalInteractionCreate, InternationalInteractionUpdate,\
    ManagementHistoryCreate, ManagementHistoryUpdate,\
    OrganizationCreate, OrganizationUpdate
from sqlalchemy.orm import Session
from pydantic.types import UUID4


class CRUDProject(CRUDBase[Project, ProjectCreate, ProjectUpdate]):
    def get_by_user_id(self, db: Session, user_id: UUID4):
        return db.query(Project).filter(Project.user_id == user_id).all()

    def remove_by_user_id(self, db: Session, user_id: UUID4):
        objs = self.get_by_user_id(db, user_id)
        for obj in objs:
            db.delete(obj)
            db.commit()
            print(obj)
        return


class CRUDInterdisciplinaryInteraction(
        CRUDBase[
            InterdisciplinaryInteraction,
            InterdisciplinaryInteractionCreate,
            InterdisciplinaryInteractionUpdate
        ]):
    def get_by_user_id(self, db: Session, user_id: UUID4):
        return db.query(InterdisciplinaryInteraction)\
            .filter(InterdisciplinaryInteraction.user_id == user_id).all()

    def remove_by_user_id(self, db: Session, user_id: UUID4):
        objs = self.get_by_user_id(db, user_id)
        for obj in objs:
            db.delete(obj)
            db.commit()
            print(obj)
        return


class CRUDNetwork(CRUDBase[Network, NetworkCreate, NetworkUpdate]):
    def get_by_user_id(self, db: Session, user_id: UUID4):
        return db.query(Network).filter(Network.user_id == user_id).all()

    def remove_by_user_id(self, db: Session, user_id: UUID4):
        objs = self.get_by_user_id(db, user_id)
        for obj in objs:
            db.delete(obj)
            db.commit()
            print(obj)
        return


class CRUDInternationalInteraction(
        CRUDBase[
            InternationalInteraction,
            InternationalInteractionCreate,
            InternationalInteractionUpdate,
        ]):
    def get_by_user_id(self, db: Session, user_id: UUID4):
        return db.query(InternationalInteraction)\
            .filter(InternationalInteraction.user_id == user_id).all()

    def remove_by_user_id(self, db: Session, user_id: UUID4):
        objs = self.get_by_user_id(db, user_id)
        for obj in objs:
            db.delete(obj)
            db.commit()
            print(obj)
        return


class CRUDManagementHistory(
        CRUDBase[
            ManagementHistory,
            ManagementHistoryCreate,
            ManagementHistoryUpdate
        ]):
    def get_by_user_id(self, db: Session, user_id: UUID4):
        return db.query(ManagementHistory)\
            .filter(ManagementHistory.user_id == user_id).all()

    def remove_by_user_id(self, db: Session, user_id: UUID4):
        objs = self.get_by_user_id(db, user_id)
        for obj in objs:
            db.delete(obj)
            db.commit()
            print(obj)
        return


class CRUDOrganization(
        CRUDBase[
            Organization,
            OrganizationCreate,
            OrganizationUpdate
        ]):
    def get_by_user_id(self, db: Session, user_id: UUID4):
        return db.query(Organization)\
            .filter(Organization.user_id == user_id).all()

    def remove_by_user_id(self, db: Session, user_id: UUID4):
        objs = self.get_by_user_id(db, user_id)
        for obj in objs:
            db.delete(obj)
            db.commit()
            print(obj)
        return


interdisciplinary_interaction = CRUDInterdisciplinaryInteraction(
    InterdisciplinaryInteraction)
international_interaction = CRUDInternationalInteraction(
    InternationalInteraction)
management_history = CRUDManagementHistory(ManagementHistory)
network = CRUDNetwork(Network)
organization = CRUDOrganization(Organization)
project = CRUDProject(Project)
