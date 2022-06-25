from uuid import uuid4

from app.db.base_class import Base
from sqlalchemy import Column, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship


class Permission(Base):
    __tablename__ = "permissions"
    id = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid4
    )
    name = Column(String(100))
    persian_name = Column(String(100))
    description = Column(Text)
    user_permission = relationship(
        "UserPermission", back_populates="permission")
