from typing import Any, List

from app import crud, schemas
from app.api import deps
from fastapi import APIRouter, Depends, Security
from app import models
from app.constants.role import Role
from sqlalchemy.orm import Session

router = APIRouter(prefix="/permission", tags=["permissions"])


@router.get("/", response_model=List[schemas.Permission])
def get_permissions(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Security(
        deps.get_current_active_user,
        scopes=[
            Role.ADMIN["name"],
            Role.ASSISTANT["name"],
            Role.SUPER_ADMIN["name"],
            Role.USER["name"]
        ],
    ),
) -> Any:
    """
    Retrieve all available user permissions.
    """
    permissions = crud.user_permission.get_by_user_id(
        db, user_id=current_user.id)
    return permissions
