from sqlalchemy.orm import relationship
from uuid import uuid4

from app.db.base_class import Base
from sqlalchemy import Column, String, Text
from sqlalchemy.dialects.postgresql import UUID


class College(Base):
    __tablename__ = "colleges"
    id = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid4
    )
    name = Column(String(100), index=True)
    description = Column(Text)
    user = relationship(
        "User", back_populates="college")


class Expertise(Base):
    __tablename__ = "expertises"
    id = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid4
    )
    name = Column(String(100), index=True)
    description = Column(Text)
    user = relationship(
        "User", back_populates="expertise")


class FieldOfStudy(Base):
    __tablename__ = "field_of_studies"
    id = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid4
    )
    name = Column(String(100), index=True)
    description = Column(Text)
    user = relationship(
        "User", back_populates="field_of_study")


class Grade(Base):
    __tablename__ = "grades"
    id = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid4
    )
    name = Column(String(100), index=True)
    description = Column(Text)
    user = relationship(
        "User", back_populates="grade")
