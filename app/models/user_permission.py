from app.db.base_class import Base
from sqlalchemy import Column, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship


class UserPermission(Base):
    __tablename__ = "user_permissions"
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        primary_key=True,
        nullable=False,
    )
    permission_id = Column(
        UUID(as_uuid=True),
        ForeignKey("permissions.id"),
        primary_key=True,
        nullable=False,
    )

    permission = relationship(
        "Permission", back_populates="user_permission")

    user = relationship(
        "User", back_populates="user_permission")

    __table_args__ = (
        UniqueConstraint("user_id", "permission_id",
                         name="unique_user_permission"),
    )
