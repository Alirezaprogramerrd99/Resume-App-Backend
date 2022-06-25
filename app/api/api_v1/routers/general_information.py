from typing import Any, List

from app import crud, schemas
from app.api import deps
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

router = APIRouter(prefix="/general", tags=["general information"])


@router.get("/college", response_model=List[schemas.College])
def get_colleges(
    db: Session = Depends(deps.get_db), skip: int = 0, limit: int = 100,
) -> Any:
    """
    Retrieve all available user roles.
    """
    items = crud.college.get_multi(db, skip=skip, limit=limit)
    return items


@router.post("/college", response_model=schemas.College)
def create_college(
    *,
    db: Session = Depends(deps.get_db),
    obj_in: schemas.CollegeCreate,
) -> Any:
    item = crud.college.create(db, obj_in=obj_in)
    return item


@router.get("/grade", response_model=List[schemas.Grade])
def get_grades(
    db: Session = Depends(deps.get_db), skip: int = 0, limit: int = 100,
) -> Any:
    """
    Retrieve all available user roles.
    """
    items = crud.grade.get_multi(db, skip=skip, limit=limit)
    return items


@router.post("/grade", response_model=schemas.Grade)
def create_grade(
    *,
    db: Session = Depends(deps.get_db),
    obj_in: schemas.GradeCreate,
) -> Any:
    item = crud.grade.create(db, obj_in=obj_in)
    return item


@router.get("/field", response_model=List[schemas.FieldOfStudy])
def get_fields(
    db: Session = Depends(deps.get_db), skip: int = 0, limit: int = 100,
) -> Any:
    """
    Retrieve all available user roles.
    """
    items = crud.field_of_study.get_multi(db, skip=skip, limit=limit)
    return items


@router.post("/field", response_model=schemas.FieldOfStudy)
def create_field(
    *,
    db: Session = Depends(deps.get_db),
    obj_in: schemas.FieldOfStudyCreate,
) -> Any:
    item = crud.field_of_study.create(db, obj_in=obj_in)
    return item


@router.get("/expertise", response_model=List[schemas.Expertise])
def get_expertises(
    db: Session = Depends(deps.get_db), skip: int = 0, limit: int = 100,
) -> Any:
    """
    Retrieve all available user roles.
    """
    items = crud.expertise.get_multi(db, skip=skip, limit=limit)
    return items


@router.post("/expertise", response_model=schemas.Expertise)
def create_expertise(
    *,
    db: Session = Depends(deps.get_db),
    obj_in: schemas.ExpertiseCreate,
) -> Any:
    item = crud.expertise.create(db, obj_in=obj_in)
    return item
