from typing import Optional

from app.crud.base import CRUDBase
from app.models.permission import Permission
from app.schemas.permission import PermissionCreate, PermissionUpdate
from sqlalchemy.orm import Session


class CRUDPermission(
    CRUDBase[Permission, PermissionCreate, PermissionUpdate]
):
    def get_by_name(self, db: Session, *, name: str) -> Optional[Permission]:
        return db.query(self.model).filter(Permission.name == name).first()


permission = CRUDPermission(Permission)
