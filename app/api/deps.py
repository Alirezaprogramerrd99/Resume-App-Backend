import logging
from typing import Generator

from app import crud, models, schemas
from app.constants.role import Role
from app.core import security
from app.core.config import settings
from app.db.session import SessionLocal
from fastapi import Depends, HTTPException, Security, status
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session
from app.constants.errors import Error
reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/auth/access-token",
    scopes={
        Role.GUEST["name"]: Role.GUEST["description"],
        Role.ADMIN["name"]: Role.ADMIN["description"],
        Role.ASSISTANT["name"]: Role.ASSISTANT["description"],
        Role.SUPER_ADMIN["name"]: Role.SUPER_ADMIN["description"],
        Role.USER["name"]: Role.USER["description"],
    },
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def get_current_user(
    security_scopes: SecurityScopes,
    db: Session = Depends(get_db),
    token: str = Depends(reusable_oauth2),
) -> models.User:
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = "Bearer"
    credentials_exception = HTTPException(
        status_code=Error.USER_PASS_WRONG_ERROR["code"],
        detail=Error.USER_PASS_WRONG_ERROR["text"],
        headers={"WWW-Authenticate": authenticate_value},
    )
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        if payload.get("id") is None:
            raise credentials_exception
        token_data = schemas.TokenPayload(**payload)    # payload is dict.
    except (jwt.JWTError, ValidationError):
        logger.error("Error Decoding Token", exc_info=True)
        raise HTTPException(
            status_code=Error.TOKEN_NOT_EXIST_OR_EXPIRATION_ERROR["code"],
            detail=Error.TOKEN_NOT_EXIST_OR_EXPIRATION_ERROR["text"],
        )
    user = crud.user.get(db, id=token_data.id)
    if not user:
        raise credentials_exception
    if security_scopes.scopes and not token_data.role:
        raise HTTPException(
            status_code=Error.PERMISSION_DENIED_ERROR["code"],
            detail=Error.PERMISSION_DENIED_ERROR["text"],
            headers={"WWW-Authenticate": authenticate_value},
        )
    if (
        security_scopes.scopes
        and token_data.role not in security_scopes.scopes
    ):
        raise HTTPException(
            status_code=Error.PERMISSION_DENIED_ERROR["code"],
            detail=Error.PERMISSION_DENIED_ERROR["text"],
            headers={"WWW-Authenticate": authenticate_value},
        )
    return user


def get_current_active_user(
    current_user: models.User = Security(get_current_user, scopes=[],),
) -> models.User:
    if not crud.user.is_active(current_user):
        raise HTTPException(
            status_code=Error.INACTIVE_USER["code"],
            detail=Error.INACTIVE_USER["text"]
        )
    return current_user
