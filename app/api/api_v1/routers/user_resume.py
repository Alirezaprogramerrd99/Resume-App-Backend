from app.constants.permission import Permission
from typing import Any

from app import crud, schemas, models
from app.api import deps
from fastapi import APIRouter, Depends, Security, HTTPException
from sqlalchemy.orm import Session
from app.constants.role import Role
from app.constants.errors import Error
from pydantic.types import UUID4
from app.api.api_v1.routers import helper

router = APIRouter(prefix="/resume", tags=["resume"])


@router.post("/", response_model=schemas.UserResume)
def create_resume(
    *,
    db: Session = Depends(deps.get_db),
    obj_in: schemas.UserResumeCreate,
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
    user_id = current_user.id
    helper.delete_resume(db, user_id)
    obj = helper.create_resume(db, obj_in, user_id)
    return obj


@router.get("/", response_model=schemas.UserResume)
def get_resume(
    *,
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
    user_id = current_user.id
    obj = helper.get_resume(db, user_id)
    return obj


@router.post("/{user_id}", response_model=schemas.UserResume)
def create_resume_by_admin(
    *,
    db: Session = Depends(deps.get_db),
    user_id: UUID4,
    obj_in: schemas.UserResumeCreate,
    current_user: models.User = Security(
        deps.get_current_active_user,
        scopes=[
            Role.ADMIN["name"],
            Role.ASSISTANT["name"],
            Role.SUPER_ADMIN["name"],
        ],
    ),
) -> Any:
    endpoint_permission_name = Permission.ADD_RESUME_FOR_USERS["name"]
    current_user_permissions = crud.user_permission.get_user_permissions_name(
        db, user_id=current_user.id)
    if endpoint_permission_name not in current_user_permissions:
        raise HTTPException(
            status_code=Error.PERMISSION_DENIED_ERROR["code"],
            detail=Error.PERMISSION_DENIED_ERROR["text"],
        )
    helper.delete_resume(db, user_id)
    obj = helper.create_resume(db, obj_in, user_id)
    return obj


@router.get("/{user_id}", response_model=schemas.UserResume)
def get_resume_by_admin(
    *,
    db: Session = Depends(deps.get_db),
    user_id: UUID4,
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

    endpoint_permission_name = Permission.GET_USER_RESUME["name"]
    current_user_permissions = crud.user_permission.get_user_permissions_name(
        db, user_id=current_user.id)
    if endpoint_permission_name not in current_user_permissions:
        raise HTTPException(
            status_code=Error.PERMISSION_DENIED_ERROR["code"],
            detail=Error.PERMISSION_DENIED_ERROR["text"],
        )
    obj = helper.get_resume(db, user_id)
    return obj
