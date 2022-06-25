from app import crud, schemas
from app.constants.role import Role
from app.constants.permission import Permission
from app.constants.grade import Grade
from app.core.config import settings
from sqlalchemy.orm import Session


def init_db(db: Session) -> None:

    # Create 1st Superuser
    # Create Role If They Don't Exist

    # Guest role
    # note that get_by_name is in crud_role file
    guest_role = crud.role.get_by_name(db, name=Role.GUEST["name"])
    if not guest_role:
        guest_role_in = schemas.RoleCreate(
            name=Role.GUEST["name"],
            description=Role.GUEST["description"],
            persian_name=Role.GUEST["persian_name"]
        )
        crud.role.create(db, obj_in=guest_role_in)

    # Super Admin role
    super_admin_role = crud.role.get_by_name(db, name=Role.SUPER_ADMIN["name"])
    if not super_admin_role:
        # RoleCreate is child of baseModel
        super_admin_role_in = schemas.RoleCreate(
            name=Role.SUPER_ADMIN["name"],
            description=Role.SUPER_ADMIN["description"],
            persian_name=Role.SUPER_ADMIN["persian_name"]
        )
        # super_admin_role_in, is the pydantic baseModel Obj (for schema) thus, in ploymorphic method 'create'
        # we need to JSONify it and convert it to dict or list so we do so.
        # in the code below role is the ORM (sqlalc) model.
        crud.role.create(db, obj_in=super_admin_role_in) 

    # Admin role
    admin_role = crud.role.get_by_name(
        db, name=Role.ADMIN["name"]
    )
    if not admin_role:
        admin_role_in = schemas.RoleCreate(
            name=Role.ADMIN["name"],
            description=Role.ADMIN["description"],
            persian_name=Role.ADMIN["persian_name"]
        )
        crud.role.create(db, obj_in=admin_role_in)

    # User role
    user_role = crud.role.get_by_name(
        db, name=Role.USER["name"]
    )
    if not user_role:
        user_role_in = schemas.RoleCreate(
            name=Role.USER["name"],
            description=Role.USER["description"],
            persian_name=Role.USER["persian_name"]
        )
        crud.role.create(db, obj_in=user_role_in)

    # Assistant role
    assistant_role = crud.role.get_by_name(
        db, name=Role.ASSISTANT["name"]
    )
    if not assistant_role:
        assistant_role_in = schemas.RoleCreate(
            name=Role.ASSISTANT["name"],
            description=Role.ASSISTANT["description"],
            persian_name=Role.ASSISTANT["persian_name"]
        )
        crud.role.create(db, obj_in=assistant_role_in)

    bachelor_grade = crud.grade.get_by_name(db, name=Grade.BACHELOR["name"])
    if not bachelor_grade:
        bachelor_grade_in = schemas.GradeCreate(
            name=Grade.BACHELOR["name"],
            description=Grade.BACHELOR["description"]
        )
        crud.grade.create(db, obj_in=bachelor_grade_in)

    master_grade = crud.grade.get_by_name(db, name=Grade.MASTER["name"])
    if not master_grade:
        master_grade_in = schemas.GradeCreate(
            name=Grade.MASTER["name"],
            description=Grade.MASTER["description"]
        )
        crud.grade.create(db, obj_in=master_grade_in)

    phd_grade = crud.grade.get_by_name(db, name=Grade.PHD["name"])
    if not phd_grade:
        phd_grade_in = schemas.GradeCreate(
            name=Grade.PHD["name"],
            description=Grade.PHD["description"]
        )
        crud.grade.create(db, obj_in=phd_grade_in)

    postdoc_grade = crud.grade.get_by_name(db, name=Grade.POSTDOC["name"])
    if not postdoc_grade:
        postdoc_grade_in = schemas.GradeCreate(
            name=Grade.POSTDOC["name"],
            description=Grade.POSTDOC["description"]
        )
        crud.grade.create(db, obj_in=postdoc_grade_in)

    user = crud.user.get_by_email(db, email=settings.FIRST_ADMIN_EMAIL)
    # fetching from role table (cause we have stored it in role db) 
    role = crud.role.get_by_name(db, name=Role.SUPER_ADMIN["name"])
    if not user:
        user = crud.user.create(
            db, email=settings.FIRST_ADMIN_EMAIL,
            password=settings.FIRST_ADMIN_PASSWORD,
            role=role.id,
        )

    # Create User Permission

    for permission in Permission.permissions:

        db_permission = crud.permission.get_by_name(
            db, name=permission['name']
        )

        if not db_permission:
            permission_in = schemas.PermissionCreate(
                name=permission["name"],
                description=permission["description"],
                persian_name=permission["persian_name"]
            )
            crud.permission.create(db, obj_in=permission_in)

    # Assign permissions to user
    user_permissions = crud.user_permission.get_by_user_id(db, user_id=user.id)
    all_permissions = crud.permission.get_multi(db)
    for permission in all_permissions:
        if permission not in user_permissions:
            user_permission_in = schemas.UserPermissionCreate(
                user_id=user.id, permission_id=permission.id)
            crud.user_permission.create(db, obj_in=user_permission_in)
