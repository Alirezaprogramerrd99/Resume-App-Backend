from typing import Any, List
from app import crud, models, schemas
from app.api import deps
from app.constants.role import Role
from app.constants.errors import Error
from app.constants.permission import Permission
from fastapi import APIRouter, Depends, HTTPException, Security, status
from sqlalchemy.orm import Session
from app.core import storage
from app.core.config import settings
from pydantic.types import UUID4
from app.api.api_v1.routers import helper
from app.core.security import get_password_hash
from app.core import cache


router_user = APIRouter(prefix="/user", tags=["user"])
router_admin = APIRouter(prefix="/admin", tags=["admin"])


@router_user.post("/register", status_code=status.HTTP_201_CREATED)
def register_user(
    *,
    db: Session = Depends(deps.get_db),
    user_in: schemas.UserRegister,
) -> Any:
    """
    register user
    """
    user = crud.user.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=Error.USER_EXIST_ERROR["code"],
            detail=Error.USER_EXIST_ERROR["text"],
        )
    # if user doesn't exist, register it into system.
    role = crud.role.get_by_name(db, name=Role.USER["name"])
    user = crud.user.user_register(db, obj_in=user_in, role_id=role.id)

    return 


@router_user.post("" , status_code= status.HTTP_201_CREATED)
def create_user(
    *,
    db: Session = Depends(deps.get_db),
    user_in: schemas.UserCreate,
    current_user: models.User = Security(
        deps.get_current_active_user,
        scopes=[
            Role.ADMIN["name"],
            Role.SUPER_ADMIN["name"],
            Role.ASSISTANT["name"],
        ],
    ),
) -> Any:
    endpoint_permission_name = Permission.ADD_USER["name"]
    current_user_permissions = crud.user_permission.get_user_permissions_name(
        db, user_id=current_user.id)
    if endpoint_permission_name not in current_user_permissions:
        raise HTTPException(
            status_code=Error.PERMISSION_DENIED_ERROR["status"],
            detail=Error.PERMISSION_DENIED_ERROR["text"],
        )

    user = crud.user.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=Error.USER_EXIST_ERROR["code"],
            detail=Error.USER_EXIST_ERROR["text"],
        )
    role = crud.role.get_by_name(db, name=Role.USER["name"])
    user = crud.user.create_user(db, obj_in=user_in, role_id=role.id)
    return user


@router_user.delete("/{user_id}", status_code=status.HTTP_200_OK)
def delete_user(
    *,
    db: Session = Depends(deps.get_db),
    user_id: UUID4,
    current_user: models.User = Security(
        deps.get_current_active_user,
        scopes=[
            Role.ADMIN["name"],
            Role.SUPER_ADMIN["name"],
            Role.ASSISTANT["name"],
        ],
    ),
) -> Any:
    endpoint_permission_name = Permission.DELETE_USER["name"]
    current_user_permissions = crud.user_permission.get_user_permissions_name(
        db, user_id=current_user.id)
    if endpoint_permission_name not in current_user_permissions:
        raise HTTPException(
            status_code=Error.PERMISSION_DENIED_ERROR["status"],
            detail=Error.PERMISSION_DENIED_ERROR["text"],
        )

    user = crud.user.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=409,
            detail="There is no user with the given id.",
        )

    helper.delete_resume(db, user_id)
    crud.user.remove(db, id=user_id)
    return


@router_user.get("/all", response_model=schemas.UserApiSchema)
def get_all_users(
    *,
    db: Session = Depends(deps.get_db),
    page: int = 1,
    page_size: int = 20,
    field_of_study: UUID4 = None,
    grade: UUID4 = None,
    college: UUID4 = None,
    expertise: UUID4 = None,
    word: str = None,
    current_user: models.User = Security(
        deps.get_current_active_user,
        scopes=[
            Role.ADMIN["name"],
            Role.SUPER_ADMIN["name"],
            Role.ASSISTANT["name"],
        ],
    ),
) -> Any:

    endpoint_permission_name = Permission.GET_USERS_RESUME_LIST["name"]
    current_user_permissions = crud.user_permission.get_user_permissions_name(
        db, user_id=current_user.id
    )
    if endpoint_permission_name not in current_user_permissions:
        raise HTTPException(
            status_code=Error.PERMISSION_DENIED_ERROR["status"],
            detail=Error.PERMISSION_DENIED_ERROR["text"],
        )
    role = crud.role.get_by_name(db, name=Role.USER["name"])
    data, pagination_data = crud.user.get_user_multi(
        db,
        page=page,
        page_size=page_size,
        role_id=role.id,
        field_of_study_id=field_of_study,
        expertise_id=expertise,
        college_id=college,
        grade_id=grade,
        word=word,
    )
    pagination = schemas.Pagination(
        page=page,
        total_pages=pagination_data["total_pages"],
    )
    user_api_schema = schemas.UserApiSchema(
        data=data,
        pagination=pagination
    )
    return user_api_schema


@router_admin.get("/", response_model=schemas.AdminApiSchema)
def get_admin_list(
    *,
    db: Session = Depends(deps.get_db),
    page: int = 1,
    page_size: int = 20,
    current_user: models.User = Security(
        deps.get_current_active_user,
        scopes=[
            Role.ADMIN["name"],
            Role.SUPER_ADMIN["name"],
            Role.ASSISTANT["name"],
        ],
    ),
) -> Any:
    endpoint_permission_name = Permission.GET_ADMINS_LIST["name"]
    current_user_permissions = crud.user_permission.get_user_permissions_name(
        db, user_id=current_user.id
    )
    if endpoint_permission_name not in current_user_permissions:
        raise HTTPException(
            status_code=Error.PERMISSION_DENIED_ERROR["status"],
            detail=Error.PERMISSION_DENIED_ERROR["text"],
        )

    data , pagination_data = crud.user.get_admin_multi(db, page=page, page_size=page_size)
    new_users = []
    for user in data:
        permissions = crud.user_permission.get_by_user_id(db, user_id=user.id)
        role = crud.role.get(db, id=user.role_id)
        user_schema = schemas.Admin(
            email=user.email,
            is_active=user.is_active,
            phone_number=user.phone_number,
            first_name=user.first_name,
            last_name=user.last_name,
            profile_image=storage.get_object_url(
                user.profile_image, settings.S3_PROFILE_BUCKET),
            profile_image_id=user.profile_image,
            gender=user.gender,
            id=user.id,
            role=role,
            created_at=user.created_at,
            updated_at=user.updated_at,
            permissions=permissions

        )
        new_users.append(user_schema)

    pagination = schemas.Pagination(
        page=page,
        total_pages=pagination_data["total_pages"],
    )
    user_api_schema = schemas.AdminApiSchema(
        data=new_users,
        pagination=pagination
    )
    return user_api_schema



@router_admin.post("/", status_code=status.HTTP_201_CREATED)
def create_admin(
    *,
    db: Session = Depends(deps.get_db),
    user_in: schemas.AdminCreate,
    current_user: models.User = Security(
        deps.get_current_active_user,
        scopes=[
            Role.ADMIN["name"],
            Role.SUPER_ADMIN["name"],
            Role.ASSISTANT["name"],
        ],
    ),
) -> Any:
    endpoint_permission_name = Permission.ADD_ADMIN["name"]
    current_user_permissions = crud.user_permission.get_user_permissions_name(
        db, user_id=current_user.id
    )
    if endpoint_permission_name not in current_user_permissions:
        raise HTTPException(
            status_code=Error.PERMISSION_DENIED_ERROR["status"],
            detail=Error.PERMISSION_DENIED_ERROR["text"],
        )

    user = crud.user.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=Error.USER_EXIST_ERROR["code"],
            detail=Error.USER_EXIST_ERROR["text"],
        )
    user = crud.user.create_admin(db, obj_in=user_in)

    for permission in user_in.permissions:
        user_permission = schemas.UserPermissionCreate(
            user_id=user.id,
            permission_id=permission
        )
        crud.user_permission.create(db, obj_in=user_permission)

    return user


@router_admin.delete("/{user_id}", status_code=status.HTTP_200_OK)
def delete_admin(
    *,
    db: Session = Depends(deps.get_db),
    user_id: UUID4,
    current_user: models.User = Security(
        deps.get_current_active_user,
        scopes=[
            Role.ADMIN["name"],
            Role.SUPER_ADMIN["name"],
            Role.ASSISTANT["name"],
        ],
    ),
) -> Any:
    endpoint_permission_name = Permission.DELETE_ADMIN["name"]
    current_user_permissions = crud.user_permission.get_user_permissions_name(
        db, user_id=current_user.id
    )
    if endpoint_permission_name not in current_user_permissions:
        raise HTTPException(
            status_code=Error.PERMISSION_DENIED_ERROR["status"],
            detail=Error.PERMISSION_DENIED_ERROR["text"],
        )

    user = crud.user.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=409,
            detail="The is no user with the given id.",
        )
    crud.user_permission.remove_by_user_id(db, user_id=user_id)
    crud.user.remove(db, id=user_id)
    return


@router_admin.put("/{user_id}", status_code=status.HTTP_200_OK)
def update_admin(
    *,
    db: Session = Depends(deps.get_db),
    user_in: schemas.AdminUpdate,
    user_id: UUID4,
    current_user: models.User = Security(
        deps.get_current_active_user,
        scopes=[
            Role.ADMIN["name"],
            Role.SUPER_ADMIN["name"],
            Role.ASSISTANT["name"],
        ],
    ),
) -> Any:
    endpoint_permission_name = Permission.UPDATE_ADMIN["name"]
    current_user_permissions = crud.user_permission.get_user_permissions_name(
        db, user_id=current_user.id
    )
    if endpoint_permission_name not in current_user_permissions:
        raise HTTPException(
            status_code=Error.PERMISSION_DENIED_ERROR["status"],
            detail=Error.PERMISSION_DENIED_ERROR["text"],
        )
    user_db = crud.user.get(db, id=user_id)
    if not user_db:
        raise HTTPException(
            status_code=Error.USER_EXIST_ERROR["code"],
            detail=Error.USER_EXIST_ERROR["text"],
        )
    crud.user.change_password(db, user_id=user_db.id,
                              new_password=user_in.new_password)

    crud.user.update_admin(db, user_id=user_db.id, obj_in=user_in)
    user_permissions = crud.user_permission.get_by_user_id(db, user_id=user_id)
    for user_permission in user_permissions:
        crud.user_permission.remove(
            db, user_id=user_db.id, permission_id=user_permission.id)

    for permission in user_in.permissions:
        user_permission = schemas.UserPermissionCreate(
            user_id=user_db.id,
            permission_id=permission
        )
        crud.user_permission.create(db, obj_in=user_permission)

    return


@router_admin.put("/",  status_code=status.HTTP_200_OK)
def update_admin_me(
    *,
    db: Session = Depends(deps.get_db),
    user_in: schemas.AdminUpdateMe,
    current_user: models.User = Security(
        deps.get_current_active_user,
        scopes=[
            Role.ADMIN["name"],
            Role.SUPER_ADMIN["name"],
            Role.ASSISTANT["name"],
        ],
    ),
) -> Any:
    user_id = current_user.id
    user_db = crud.user.get(db, id=user_id)
    if user_in.old_password:
        if not get_password_hash(
                user_in.old_password) == user_db.hashed_password:
            raise HTTPException(
                status_code=Error.PERMISSION_DENIED_ERROR["code"],
                detail=Error.PERMISSION_DENIED_ERROR["text"],
            )
        crud.user.change_password(
            db, user_id=user_id, new_password=user_in.new_password)

    crud.user.update_admin_me(db, user_id=user_id, obj_in=user_in)

    return


@router_admin.get("/me", response_model=schemas.AdminGetMe)
def get_admin_me(
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Security(
        deps.get_current_active_user,
        scopes=[
            Role.ADMIN["name"],
            Role.SUPER_ADMIN["name"],
            Role.ASSISTANT["name"],
        ],
    ),
) -> Any:
    user_id = current_user.id

    user_db = crud.user.get(db, id=user_id)
    profile_image_id = user_db.profile_image
    if user_db.profile_image not in [None, ""]:
        user_db.profile_image = storage.get_object_url(
            user_db.profile_image, settings.S3_PROFILE_BUCKET)
    user = schemas.AdminGetMe(
        email=user_db.email,
        is_active=user_db.is_active,
        phone_number=user_db.phone_number,
        first_name=user_db.first_name,
        last_name=user_db.last_name,
        profile_image=user_db.profile_image,
        gender=user_db.gender,
        profile_image_id=profile_image_id
    )
    return user


@router_user.post("/forget-password", status_code=status.HTTP_200_OK)
async def forget_password(
    *,
    db: Session = Depends(deps.get_db),
    user_in: schemas.ForgetPassword,
):
    user = crud.user.get_by_email(db, email=user_in.email)
    if user is None:
        raise HTTPException(
            status_code=Error.USER_NOT_FOUND['code'],
            detail=Error.USER_NOT_FOUND['text'],
        )
    await crud.user.send_recovery_mail(db, user.email)


@router_user.post("/recovery-password", status_code=status.HTTP_200_OK)
def recovery_password(
    *,
    db: Session = Depends(deps.get_db),
    user_in: schemas.ChangePassword
):
    client = cache.get_redis_connection()
    code = client.get(user_in.email)
    if code is None:
        raise HTTPException(
            status_code=Error.CODE_EXPIRATION_OR_NOT_EXIST_ERROR["code"],
            detail=Error.CODE_EXPIRATION_OR_NOT_EXIST_ERROR["text"],
        )
    if str(code.decode('utf-8')) != str(user_in.code):
        raise HTTPException(
            status_code=Error.CODE_EXPIRATION_OR_NOT_EXIST_ERROR["code"],
            detail=Error.CODE_EXPIRATION_OR_NOT_EXIST_ERROR["text"],
        )
    user = crud.user.get_by_email(db, email=user_in.email)
    crud.user.change_password(
        db, user_id=user.id, new_password=user_in.new_password)
    return


@router_user.get("/delete-for-test/{email}", status_code=status.HTTP_200_OK)
def recovery_password(
    *,
    db: Session = Depends(deps.get_db),
    email: str = None
):
    user = crud.user.get_by_email(db, email=email)
    crud.user.remove(db, id=user.id)
    return
