from http.client import HTTPException
from typing import Any, List
from app import crud, schemas, models
from app.api import deps
from fastapi import APIRouter, Depends, Security
from sqlalchemy.orm import Session
from app.constants.role import Role
from app.constants.grade import Grade
import jdatetime
import datetime


router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/gender", response_model=schemas.UserGender)
def get_user_gender(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Security(
        deps.get_current_active_user,
        scopes=[
            Role.ADMIN["name"],
            Role.ASSISTANT["name"],
            Role.SUPER_ADMIN["name"],
        ],
    ),
) -> Any:
    male_count, female_count = crud.dashboard.get_users_count_based_on_gender(
        db=db)
    obj = schemas.UserGender(
        male_count=male_count,
        female_count=female_count
    )
    return obj


@router.get("/grade", response_model=List[schemas.UserGrade])
def get_user_grade(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Security(
        deps.get_current_active_user,
        scopes=[
            Role.ADMIN["name"],
            Role.ASSISTANT["name"],
            Role.SUPER_ADMIN["name"],
        ],
    ),
) -> Any:
    bachelor_id = crud.grade.get_by_name(db, name=Grade.BACHELOR["name"]).id
    master_id = crud.grade.get_by_name(db, name=Grade.MASTER["name"]).id
    phd_id = crud.grade.get_by_name(db, name=Grade.PHD["name"]).id
    postdoc_id = crud.grade.get_by_name(db, name=Grade.POSTDOC["name"]).id

    bachelor_count = crud.dashboard.get_users_count_based_on_grade(
        db, grade_id=bachelor_id)
    master_count = crud.dashboard.get_users_count_based_on_grade(
        db, grade_id=master_id)
    phd_count = crud.dashboard.get_users_count_based_on_grade(
        db, grade_id=phd_id)
    postdoc_count = crud.dashboard.get_users_count_based_on_grade(
        db, grade_id=postdoc_id)
    return[
        schemas.UserGrade(
            name=Grade.BACHELOR["name"],
            count=bachelor_count
        ),
        schemas.UserGrade(
            name=Grade.MASTER["name"],
            count=master_count
        ),
        schemas.UserGrade(
            name=Grade.PHD["name"],
            count=phd_count
        ),
        schemas.UserGrade(
            name=Grade.POSTDOC["name"],
            count=postdoc_count
        ),
    ]


@router.post("/user-reister")
def get_user_register(
    db: Session = Depends(deps.get_db),
    *,
    obj_in: schemas.DashboardUserRegisterIn,
    current_user: models.User = Security(
        deps.get_current_active_user,
        scopes=[
            Role.ADMIN["name"],
            Role.ASSISTANT["name"],
            Role.SUPER_ADMIN["name"],
        ],
    ),
) -> Any:

    if obj_in.chart_type == "yearly":
        response = []
        for i in range(1, 13):
            month_end_day = 0
            if i in [1, 2, 3, 4, 5, 6]:
                month_end_day = 31
            elif i in [7, 8, 9, 10, 11]:
                month_end_day = 30
            else:
                month_end_day = 29

            start_date = jdatetime.JalaliToGregorian(
                jyear=obj_in.year, jmonth=i, jday=1)

            end_date = jdatetime.JalaliToGregorian(
                jyear=obj_in.year, jmonth=i, jday=month_end_day)

            g_start_date = datetime.datetime(
                year=start_date.gyear, month=start_date.gmonth, day=start_date.gday)

            g_end_date = datetime.datetime(
                year=end_date.gyear, month=end_date.gmonth, day=end_date.gday)

            count = crud.user.get_user_count_between_dates(
                db, g_start_date, g_end_date)

            response.append({
                "month": i,
                "count": count
            })
        return response

    elif obj_in.chart_type == "monthly":
        response = []
        days_of_month = None
        if obj_in.month in [1, 2, 3, 4, 5, 6]:
            days_of_month = 31
        elif obj_in.month in [7, 8, 9, 10, 11]:
            days_of_month = 30
        elif obj_in.month == 12:
            days_of_month = 29
        else:
            raise HTTPException(
                status_code=400,
            )
        for i in range(1, days_of_month + 1):
            jdatetime.datetime
            
            start_date_time = jdatetime.datetime(year=obj_in.year, month=obj_in.month , day = i)

            g_start_date_time = jdatetime.datetime.togregorian(start_date_time)

            g_end_date_time = g_start_date_time + datetime.timedelta(days=1)

            

            count = crud.user.get_user_count_between_dates(db, g_start_date_time, g_end_date_time)
            
            response.append(
                {
                    "day_of_month" : i,
                    "count" : count,
                }
            )
        return response


    else:
        raise HTTPException(
            status_code=404
        )
