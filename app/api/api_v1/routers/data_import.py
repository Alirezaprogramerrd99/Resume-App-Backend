from fastapi import UploadFile, File, APIRouter, Security
from app import models, crud, schemas
from app.api import deps
from app.constants.role import Role
import uuid
from app.core import storage
from app.core.config import settings
from .helper import create_resume
from app.api.api_v1.routers import helper
from app.api import deps
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import pandas as pd
router = APIRouter(prefix="/data", tags=["data"])


@router.post("/add")
def add_resume(
    db: Session = Depends(deps.get_db),

):
    df = pd.read_excel("data.xlsx")
    role = crud.role.get_by_name(db, name=Role.USER["name"])
    for i, item in df.iterrows():
        if type(item[4]) != float:

            try:
                mobile = str(item[5])[0:10]
                mobile = f"0{mobile}"
                if len(str(item[5])) < 10:
                    mobile = None
                user = crud.user.create_user(db, obj_in=schemas.UserCreate(
                    email=item[4],
                    is_active=True,
                    phone_number=mobile,
                    first_name=item[2],
                    last_name=item[3],
                    password=item[5],
                ), role_id=role.id)

                international_interaction = item[10]
                international_interactions = []
                if international_interaction and type(international_interaction) == str:
                    for i in international_interaction.split("\n"):
                        if len(str(i)) > 5:
                            international_interactions.append(
                                schemas.InternationalInteractionResumeCreate(
                                    title=str(i)
                                )
                            )

                interdisciplinary_interaction = item[9]
                interdisciplinary_interactions = []
                if interdisciplinary_interaction and type(interdisciplinary_interaction) == str:
                    for i in interdisciplinary_interaction.split("\n"):
                        if len(str(i)) > 2:
                            interdisciplinary_interactions.append(
                                schemas.InterdisciplinaryInteractionResumeCreate(
                                    title=str(i)
                                )
                            )

                network = item[11]
                networks = []
                if network and type(network) == str:
                    for i in network.split("\n"):
                        if len(str(i)) > 2:
                            networks.append(
                                schemas.NetworkResumeCreate(
                                    title=str(i)
                                )
                            )

                project = item[8]
                projects = []

                if project and type(project) == str:
                    for i in project.split("\n"):
                        if len(str(i)) > 2:
                            projects.append(
                                schemas.ProjectResumeCreate(
                                    title=str(i)
                                )
                            )

                management = item[12]
                managements = []

                if management and type(management) == str:
                    for i in management.split("\n"):
                        if len(str(i)) > 2:
                            managements.append(
                                schemas.ManagementHistoryResumeCreate(
                                    project_organization_name=str(i)
                                )
                            )

                organization = item[13]
                organizations = []

                if organization and type(organization) == str:
                    for i in organization.split("\n"):
                        if len(str(i)) > 2:
                            organizations.append(
                                schemas.OrganizationResumeCreate(
                                    organization_name=str(i)
                                )
                            )

                resume = schemas.UserResumeCreate(
                        international_interactions=international_interactions,
                        interdisciplinary_interactions=interdisciplinary_interactions,  # noqa
                        projects=projects,
                        networks=networks,
                        management_histories=managements,
                        organizations=organizations
                )
                helper.create_resume(db, obj_in=resume, user_id=user.id)
            except Exception as e:
                print(e)


@router.post("/remove")
def delete_all_resume(
    db: Session = Depends(deps.get_db),

):
    users = db.query(models.User).filter(
        models.User.email != settings.FIRST_ADMIN_EMAIL).all()
    for user in users:
        crud.user.remove(db, id=user.id)
        # helper.delete_resume(db , user_id = user.id)
