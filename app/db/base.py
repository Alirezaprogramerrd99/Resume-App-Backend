# Import all the models, so that Base has them before being
# imported by Alembic
from app.db.base_class import Base  # noqa
from app.models.role import Role  # noqa
from app.models.user import User  # noqa
from app.models.permission import Permission  # noqa
from app.models.user_permission import UserPermission  # noqa
from app.models.general_information import College, Grade  # noqa
from app.models.resume import ManagementHistory, Organization,\
    Network, InterdisciplinaryInteraction, InternationalInteraction,\
         Project, Expertise, FieldOfStudy  # noqa
