from typing import Any, List

from app import crud, schemas
from app.api import deps
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.constants.role import Role


router = APIRouter(prefix="/roles", tags=["roles"])


@router.get("/", response_model=List[schemas.Role])
def get_roles(
    db: Session = Depends(deps.get_db)
) -> Any:
    """
    Retrieve all available user roles.
    """

    admin = crud.role.get_by_name(db, name=Role.ADMIN["name"])
    assistant = crud.role.get_by_name(db, name=Role.ASSISTANT["name"])
    super_admin = crud.role.get_by_name(db, name=Role.SUPER_ADMIN["name"])
    return [super_admin, admin, assistant]
