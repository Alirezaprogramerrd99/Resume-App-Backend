from typing import Any

from app import crud, schemas
from sqlalchemy.orm import Session
from app.core import storage
from jdatetime import date as jdate
import jdatetime
import datetime


def delete_resume(
    db: Session,
    user_id,
):
    crud.international_interaction.remove_by_user_id(db, user_id=user_id)
    crud.interdisciplinary_interaction.remove_by_user_id(db, user_id=user_id)
    crud.project.remove_by_user_id(db, user_id=user_id)
    crud.network.remove_by_user_id(db, user_id=user_id)
    crud.management_history.remove_by_user_id(db, user_id=user_id)
    crud.organization.remove_by_user_id(db, user_id=user_id)


def create_resume(
    db: Session,
    obj_in: schemas.UserResumeCreate,
    user_id
) -> Any:
    user = crud.user.get(db, id=user_id)

    user_in = schemas.UserUpdate(
        email=obj_in.email,
        is_active=True,
        phone_number=obj_in.phone_number,
        first_name=obj_in.first_name,
        last_name=obj_in.last_name,
        profile_image=obj_in.profile_image,
        gender=obj_in.gender,
        field_of_study_id=obj_in.field_of_study_id,
        grade_id=obj_in.grade_id,
        expertise_id=obj_in.expertise_id,
        college_id=obj_in.college_id,
    )
    crud.user.update(db, db_obj=user, obj_in=user_in)

    for ii in obj_in.international_interactions:
        obj = schemas.InternationalInteractionCreate(
            title=ii.title,
            user_id=user_id
        )
        crud.international_interaction.create(db, obj_in=obj)

    for ii in obj_in.interdisciplinary_interactions:
        obj = schemas.InterdisciplinaryInteractionCreate(
            title=ii.title,
            user_id=user_id
        )
        crud.interdisciplinary_interaction.create(db, obj_in=obj)

    for network in obj_in.networks:
        obj = schemas.NetworkCreate(
            title=network.title,
            user_id=user_id,
        )
        crud.network.create(db, obj_in=obj)

    for history in obj_in.management_histories:
        obj = schemas.ManagementHistoryCreate(
            position=history.position,
            project_organization_name=history.project_organization_name,
            user_id=user_id
        )
        crud.management_history.create(db, obj_in=obj)

    for project in obj_in.projects:
        year = int(project.date[0:4])
        month = int(project.date[5:7])
        day = int(project.date[8:10])
        gdate = jdatetime.JalaliToGregorian(jyear=year, jmonth=month, jday=day)
        date = datetime.datetime(
            year=gdate.gyear,
            month=gdate.gmonth,
            day=gdate.gday,
            hour=0,
            minute=0,
            second=0
        )
        obj = schemas.ProjectCreate(
            title=project.title,
            employer=project.employer,
            date=date,
            description=project.description,
            user_id=user_id
        )
        crud.project.create(db, obj_in=obj)

    for organization in obj_in.organizations:
        obj = schemas.OrganizationCreate(
            position=organization.position,
            organization_name=organization.organization_name,
            user_id=user_id
        )
        crud.organization.create(db, obj_in=obj)

    user = crud.user.get(db, id=user_id)
    # user.profile_image = storage.get_object_url(
    #     user.profile_image
    # )
    user_resume = schemas.UserResume(
        international_interactions=obj_in.international_interactions,
        interdisciplinary_interactions=obj_in.interdisciplinary_interactions,
        projects=obj_in.projects,
        networks=obj_in.networks,
        management_histories=obj_in.management_histories,
        organizations=obj_in.organizations,
        user=user,
    )
    return user_resume


def get_resume(db: Session, user_id):
    user = crud.user.get(db, id=user_id)

    international_interactions = crud.international_interaction.get_by_user_id(
        db, user_id=user_id)

    new_international_interactions = []
    for ii in international_interactions:
        item = schemas.InternationalInteractionResumeCreate(
            title=ii.title
        )
        new_international_interactions.append(item)

    # -----------------------------------
    interdisciplinary_interactions = crud.\
        interdisciplinary_interaction.get_by_user_id(
            db, user_id=user_id)

    new_interdisciplinary_interactions = []
    for ii in interdisciplinary_interactions:
        item = schemas.InterdisciplinaryInteractionResumeCreate(
            title=ii.title
        )
        new_interdisciplinary_interactions.append(item)

    # -----------------------------------
    new_projects = []
    projects = crud.project.get_by_user_id(db, user_id=user_id)
    for p in projects:
        datem = datetime.datetime.strptime(str(p.date), "%Y-%m-%d %H:%M:%S")
        j_date = jdate.fromgregorian(
            year=datem.year, month=datem.month, day=datem.day)
        item = schemas.ProjectResumeCreate(
            title=p.title,
            employer=p.employer,
            date=str(j_date),
            description=p.description
        )
        new_projects.append(item)

    networks = crud.network.get_by_user_id(db, user_id=user_id)
    new_networks = []
    for n in networks:
        item = schemas.NetworkResumeCreate(
            title=n.title,
        )
        new_networks.append(item)

    management_histories = crud.management_history.get_by_user_id(
        db, user_id=user_id)
    new_managements = []
    for m in management_histories:
        item = schemas.ManagementHistoryResumeCreate(
            position=m.position,
            project_organization_name=m.project_organization_name
        )
        new_managements.append(item)

    organizations = crud.organization.get_by_user_id(db, user_id=user_id)
    new_organizations = []

    for org in organizations:
        item = schemas.OrganizationResumeCreate(
            position=org.position,
            organization_name=org.organization_name,
        )
        new_organizations.append(item)

    user = crud.user.get(db, id=user_id)
    user_resume = schemas.UserResume(
        international_interactions=new_international_interactions,
        interdisciplinary_interactions=new_interdisciplinary_interactions,
        projects=new_projects,
        networks=new_networks,
        management_histories=new_managements,
        organizations=new_organizations,
        user=user,
    )
    return user_resume
