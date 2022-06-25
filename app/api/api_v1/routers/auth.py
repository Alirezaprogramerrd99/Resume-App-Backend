from datetime import timedelta
from typing import Any

from app import crud, models, schemas
from app.api import deps
from app.core import security
from app.core.config import settings
from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.constants.errors import Error

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/access-token", response_model=schemas.Token)
def login_access_token(
    db: Session = Depends(deps.get_db),
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = crud.user.authenticate(
        db, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=Error.USER_PASS_WRONG_ERROR["code"],
            detail=Error.USER_PASS_WRONG_ERROR["text"],
        )
    elif not crud.user.is_active(user):
        raise HTTPException(status_code=400, detail="Inactive user")
    access_token_expires = timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    if not user.role_id:
        role = "GUEST"
    else:
        role = crud.role.get(db, id=user.role_id)
        role = role.name
    token_payload = {
        "id": str(user.id),
        "role": role,
    }
    return {
        "access_token": security.create_access_token(
            token_payload, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }


@router.post("/test-token", response_model=schemas.User)
def test_token(
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Test access token
    """
    return current_user


@router.post("/hash-password", response_model=str)
def hash_password(password: str = Body(..., embed=True),) -> Any:
    """
    Hash a password
    """
    return security.get_password_hash(password)


@router.post("/login", response_model=schemas.Login)
def login(
    db: Session = Depends(deps.get_db),
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> Any:
    user = crud.user.authenticate(
        db, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=Error.USER_PASS_WRONG_ERROR["code"],
            detail=Error.USER_PASS_WRONG_ERROR["text"],
        )
    elif not crud.user.is_active(user):
        raise HTTPException(
            status_code=Error.INACTIVE_USER["code"],
            detail=Error.INACTIVE_USER["text"],
        )
    access_token_expires = timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    if not user.role_id:
        role = "GUEST"
    else:
        role = crud.role.get(db, id=user.role_id)
        role = role.name
    token_payload = {
        "id": str(user.id),
        "role": role,
    }
    role = crud.role.get(db, id=user.role_id)

    return {
        "access_token": security.create_access_token(
            token_payload, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
        "role": role
    }
