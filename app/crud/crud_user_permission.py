from typing import Optional, List, Any

from app.crud.base import CRUDBase
from app.models.user_permission import UserPermission
from app.models.permission import Permission
from app.schemas.user_permission import UserPermissionCreate,\
    UserPermissionUpdate
from pydantic.types import UUID4
from sqlalchemy.orm import Session


class CRUDUserPermission(
    CRUDBase[UserPermission, UserPermissionCreate, UserPermissionUpdate]
):
    def get_by_user_id(
        self, db: Session, *, user_id: UUID4
    ) -> Optional[List[Permission]]:
        user_permissions = db.query(UserPermission).filter(
            UserPermission.user_id == user_id).all()
        permissions = []
        for user_permission in user_permissions:
            permission = db.query(Permission).filter(
                Permission.id == user_permission.permission_id).first()
            permissions.append(permission)

        return permissions

    def get_user_permissions_name(
        self, db: Session, *, user_id: UUID4
    ) -> Any:
        user_permissions = db.query(UserPermission).filter(
            UserPermission.user_id == user_id).all()
        permissions = []
        for user_permission in user_permissions:
            permission = db.query(Permission).filter(
                Permission.id == user_permission.permission_id).first()
            permissions.append(permission.name)

        return permissions

    def remove_by_user_id(
        self, db: Session, *, user_id: UUID4
    ) -> Any:
        user_permissions = db.query(UserPermission).filter(
            UserPermission.user_id == user_id).all()
        for user_permission in user_permissions:
            self.remove(db, user_id=user_permission.user_id,
                        permission_id=user_permission.permission_id)

    def remove(
        self, db: Session, *, user_id: UUID4, permission_id: UUID4
    ) -> Any:
        user_permission = db.query(UserPermission).filter(
            UserPermission.user_id == user_id and
            UserPermission.permission_id == permission_id).first()
        db.delete(user_permission)
        db.commit()
        return


user_permission = CRUDUserPermission(UserPermission)
