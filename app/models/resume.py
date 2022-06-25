from uuid import uuid4

from app.db.base_class import Base
from sqlalchemy import Column, DateTime, String, Text, ForeignKey, Date
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship


class Project(Base):

    __tablename__ = "projects"
    id = Column(
        UUID(as_uuid=True), primary_key=True, index=True, default=uuid4
    )
    title = Column(String(255), nullable=True)
    employer = Column(String(255), nullable=True)
    date = Column(Date, nullable=True)
    description = Column(Text, nullable=True)

    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        primary_key=True,
        nullable=True,
    )

    user = relationship("User")


class InterdisciplinaryInteraction (Base):

    __tablename__ = "interdisciplinary_interactions"
    id = Column(
        UUID(as_uuid=True), primary_key=True, index=True, default=uuid4
    )
    title = Column(String(255), nullable=True)

    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        primary_key=True,
        nullable=True,
    )

    user = relationship("User")


class Network(Base):

    __tablename__ = "networks"
    id = Column(
        UUID(as_uuid=True), primary_key=True, index=True, default=uuid4
    )
    title = Column(String(255), nullable=True)

    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        primary_key=True,
        nullable=True,
    )

    user = relationship("User")


class InternationalInteraction(Base):

    __tablename__ = "international_interactions"
    id = Column(
        UUID(as_uuid=True), primary_key=True, index=True, default=uuid4
    )

    title = Column(String(255), nullable=True)

    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        primary_key=True,
        nullable=True,
    )

    user = relationship("User")


class ManagementHistory(Base):

    __tablename__ = "management_histories"
    id = Column(
        UUID(as_uuid=True), primary_key=True, index=True, default=uuid4
    )

    position = Column(String(255), nullable=True)
    project_organization_name = Column(String(255), nullable=True)

    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        primary_key=True,
        nullable=True,
    )

    user = relationship("User")


class Organization(Base):

    __tablename__ = "organizations"
    id = Column(
        UUID(as_uuid=True), primary_key=True, index=True, default=uuid4
    )

    position = Column(String(255), nullable=True)
    organization_name = Column(String(255), nullable=True)

    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        primary_key=True,
        nullable=True,
    )

    user = relationship("User")
