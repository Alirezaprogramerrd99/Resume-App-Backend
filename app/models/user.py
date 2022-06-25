import datetime
from uuid import uuid4

from app.db.base_class import Base
from sqlalchemy import Boolean, Column, DateTime, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship


class User(Base):
    """
    Database Model for an application user
    """

    __tablename__ = "users"
    id = Column(
        UUID(as_uuid=True), primary_key=True, index=True, default=uuid4
    )
    first_name = Column(String(255), nullable=True)
    last_name = Column(String(255), nullable=True)
    gender = Column(String(5), nullable=True)
    email = Column(String(100), unique=True, nullable=False)
    profile_image = Column(String(255), nullable=True)
    phone_number = Column(String(13), nullable=True)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean(), default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(
        DateTime,
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow,
    )

    field_of_study_id = Column(
        UUID(as_uuid=True),
        ForeignKey("field_of_studies.id"),
        nullable=True,
    )
    grade_id = Column(
        UUID(as_uuid=True),
        ForeignKey("grades.id"),
        nullable=True,

    )
    college_id = Column(
        UUID(as_uuid=True),
        ForeignKey("colleges.id"),
        nullable=True,
    )
    expertise_id = Column(
        UUID(as_uuid=True),
        ForeignKey("expertises.id"),
        nullable=True,
    )

    role_id = Column(
        UUID(as_uuid=True),
        ForeignKey("roles.id"),
        nullable=True,
    )

    field_of_study = relationship(
        "FieldOfStudy", back_populates="user")
    grade = relationship("Grade", back_populates="user")
    college = relationship(
        "College", back_populates="user")
    expertise = relationship(
        "Expertise", back_populates="user")

    role = relationship(
        "Role", back_populates="user")

    user_permission = relationship(
        "UserPermission", back_populates="user")

    # resume
    project = relationship("Project", back_populates="user")
    interdisciplinary_interaction = relationship(
        "InterdisciplinaryInteraction", back_populates="user")
    network = relationship("Network", back_populates="user")
    international_interaction = relationship(
        "InternationalInteraction", back_populates="user")
    management_history = relationship(
        "ManagementHistory", back_populates="user")
    organization = relationship("Organization", back_populates="user")
