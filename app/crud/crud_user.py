from datetime import timedelta
from random import randint
from typing import Any, List, Optional

from app.core.security import get_password_hash, verify_password
from app.crud.base import CRUDBase
from app.models.user import User
from app.models.role import Role as RoleModel
from app.constants.role import Role
from app.schemas.user import AdminUpdate, AdminUpdateMe,\
    UserCreate, UserUpdate, UserRegister, AdminCreate
from sqlalchemy.orm import Session
from app.core.config import settings
from pydantic.types import UUID4
from app.models.resume import ManagementHistory, InternationalInteraction,\
    InterdisciplinaryInteraction, Project, Network, Organization
from app.core import email, storage, cache
from sqlalchemy import or_, and_


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def get_by_email(self, db: Session, *, email: str) -> Optional[User]:
        return db.query(self.model).filter(User.email == email).first()

    def user_register(
        self,
        db: Session,
        *,
        obj_in: UserRegister,
        role_id: UUID4
    ) -> User:
        # like model with type of User
        db_obj = User(
            email=obj_in.email,
            hashed_password=get_password_hash(obj_in.password),
            first_name=obj_in.first_name,
            last_name=obj_in.last_name,
            role_id=role_id,
            is_active=True
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def create_user(
        self,
        db: Session,
        *,
        obj_in: UserCreate,
        role_id
    ) -> User:
        user_db_obj = User(
            email=obj_in.email,
            hashed_password=get_password_hash(obj_in.password),
            phone_number=obj_in.phone_number,
            is_active=obj_in.is_active,
            profile_image=obj_in.profile_image,
            gender=obj_in.gender,
            first_name=obj_in.first_name,
            last_name=obj_in.last_name,
            field_of_study_id=obj_in.field_of_study_id,
            grade_id=obj_in.grade_id,
            college_id=obj_in.college_id,
            expertise_id=obj_in.expertise_id,
            role_id=role_id
        )
        db.add(user_db_obj)
        db.commit()
        db.refresh(user_db_obj)
        return

    def create_admin(
        self,
        db: Session,
        *,
        obj_in: AdminCreate
    ) -> AdminCreate:
        admin_db_object = User(
            email=obj_in.email,
            hashed_password=get_password_hash(obj_in.password),
            is_active=obj_in.is_active,
            phone_number=obj_in.phone_number,
            first_name=obj_in.first_name,
            last_name=obj_in.last_name,
            profile_image=obj_in.profile_image,
            gender=obj_in.gender,
            role_id=obj_in.role_id
        )
        db.add(admin_db_object)
        db.commit()
        db.refresh(admin_db_object)

        return admin_db_object

    def create(self, db: Session, *, email, password, role) -> User:
        user_db_obj = User(
            email=email,
            hashed_password=get_password_hash(password),
            role_id=role
        )
        db.add(user_db_obj)
        db.commit()
        db.refresh(user_db_obj)
        return user_db_obj

    def update_admin(
        self,
        db: Session,
        *,
        user_id: UUID4,
        obj_in: AdminUpdate
    ) -> User:
        db_user = db.query(User).filter(User.id == user_id).first()
        db_user.first_name = obj_in.first_name
        db_user.last_name = obj_in.last_name
        db_user.email = obj_in.email
        db_user.phone_number = obj_in.phone_number
        db_user.role_id = obj_in.role_id
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    def update_admin_me(
        self,
        db: Session,
        *,
        user_id: UUID4,
        obj_in: AdminUpdateMe
    ) -> User:
        db_user = db.query(User).filter(User.id == user_id).first()
        db_user.first_name = obj_in.first_name
        db_user.last_name = obj_in.last_name
        db_user.email = obj_in.email
        db_user.phone_number = obj_in.phone_number
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    def change_password(
        self,
        db: Session,
        *,
        user_id: UUID4,
        new_password: str
    ):
        db_user = db.query(User).filter(User.id == user_id).first()
        db_user.hashed_password = get_password_hash(new_password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    def get_user_multi(
        self, db: Session, *, page: int = 1,
        page_size: int = 20, role_id: UUID4,
        grade_id: UUID4 = None, field_of_study_id: UUID4 = None,
        expertise_id: UUID4 = None, college_id: UUID4 = None,
        word: str = None
    ):

        queryset = db.query(User).filter(User.role_id == role_id)

        if grade_id:
            queryset = queryset.filter(User.grade_id == grade_id)

        if expertise_id:
            queryset = queryset.filter(User.expertise_id == expertise_id)
        if college_id:
            queryset = queryset.filter(User.college_id == college_id)
        if field_of_study_id:
            queryset = queryset.filter(
                User.field_of_study_id == field_of_study_id)

        users = []
        if word:
            users_1 = db.query(Organization).filter(
                or_(Organization.position.like(f"%{word}%"),
                    Organization.organization_name.like(f"%{word}%"))
            ).with_entities(Organization.user_id).all()

            users_2 = db.query(ManagementHistory).filter(
                or_(ManagementHistory.project_organization_name.like(f"%{word}%") |
                    ManagementHistory.position.like(f"%{word}%"))
            ).with_entities(ManagementHistory.user_id).all()

            users_3 = db.query(InternationalInteraction).filter(
                InternationalInteraction.title.like(f"%{word}%")
            ).with_entities(InternationalInteraction.user_id).all()

            users_4 = db.query(Network).filter(
                Network.title.like(f"%{word}%")
            ).with_entities(Network.user_id).all()

            users_5 = db.query(InterdisciplinaryInteraction).filter(
                InterdisciplinaryInteraction.title.like(f"%{word}%")
            ).with_entities(InterdisciplinaryInteraction.user_id).all()

            users_6 = db.query(Project).filter(
                or_(Project.title.like(f"%{word}%") |
                    Project.description.like(f"%{word}%") |
                    Project.employer.like(f"%{word}%"))
            ).with_entities(Project.user_id).all()

            users = [*users_1, *users_2, *users_3,
                     *users_4, *users_5, *users_6]
            users = list(set(users))
            users = [str(u[0]) for u in users]

            if len(users):
                queryset = queryset.filter(User.id.in_(users))

        # pagination
        skip = (page - 1) * page_size
        all_count = queryset.count()
        total_pages = all_count / page_size
        if not total_pages.is_integer():
            total_pages += 1
        pagination_data = dict(total_pages=int(total_pages))

        # reading data

        queryset = queryset.offset(skip).limit(page_size).all()

        new_users = []
        for user in queryset:
            user.profile_image = storage.get_object_url(
                user.profile_image, settings.S3_PROFILE_BUCKET)
            new_users.append(user)

        return new_users, pagination_data

    def get_admin_multi(
        self, db: Session, *, page: int = 1, page_size: int = 20
    ):
        role_admin = db.query(RoleModel).filter(
            RoleModel.name == Role.ADMIN["name"]).first()
        role_super_admin = db.query(RoleModel).filter(
            RoleModel.name == Role.SUPER_ADMIN["name"]).first()
        role_assistant = db.query(RoleModel).filter(
            RoleModel.name == Role.ASSISTANT["name"]).first()
        queryset = db.query(User).filter(
            or_(
                User.role_id == role_super_admin.id,
                User.role_id == role_assistant.id,
                User.role_id == role_admin.id)
        )

        # pagination
        skip = (page - 1) * page_size
        all_count = queryset.count()
        total_pages = all_count / page_size
        if not total_pages.is_integer():
            total_pages += 1
        pagination_data = dict(total_pages=int(total_pages))

        # reading data
        queryset = queryset.offset(skip).limit(page_size).all()

        return queryset, pagination_data

    def authenticate(
        self, db: Session, *, email: str, password: str
    ) -> Optional[User]:
        user = self.get_by_email(db, email=email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    def is_active(self, user: User) -> bool:
        return user.is_active

    def change_status(self, db: Session, *, id: str) -> Optional[User]:
        user = db.query(User).filter(User.id == id).first()
        user.is_active = not user.is_active
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    def get(self, db: Session, id: UUID4) -> Optional[User]:
        user = db.query(User).filter(User.id == id).first()
        return user

    def get_user_count_between_dates(self, db: Session, start_date, end_date):
        return db.query(User).\
            filter(
                and_(
                    User.created_at >= start_date,
                    User.created_at <= end_date
                )
        ).count()

    def get_user_count_in_date(self, db: Session, start , end):
        return db.query(User).\
            filter(
                and_(
                    User.created_at >= start,
                    User.created_at < end
                )
        ).count()

    async def send_recovery_mail(self, db: Session, email_address: UUID4):
        code = randint(1000, 9999)
        client = cache.get_redis_connection()
        client.set(email_address, code)
        client.expire(email_address, timedelta(
            minutes=settings.FORGET_PASSWORD_CODE_EXPIRATION))
        await email.send_email("Password Recovery", [email_address], code)
        return


user = CRUDUser(User)
