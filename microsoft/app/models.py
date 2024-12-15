import uuid

from sqlalchemy import (
    Enum,
    ForeignKey,
    String,
)
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import Mapped, mapped_column, relationship

from microsoft.enums import ProjectStatus
from microsoft.app.base_model import BaseModel


class DBClient(BaseModel):
    __tablename__ = "clients"

    id: Mapped[uuid.UUID] = mapped_column(
        postgresql.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    phone: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    projects = relationship(
        "DBProject", back_populates="client"
    )  # Correct relationship


class DBProject(BaseModel):
    __tablename__ = "projects"

    id: Mapped[uuid.UUID] = mapped_column(
        postgresql.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=True)
    status: Mapped[ProjectStatus] = mapped_column(
        Enum(ProjectStatus), nullable=False, default=ProjectStatus.OPEN
    )
    client_id: Mapped[uuid.UUID] = mapped_column(
        postgresql.UUID(as_uuid=True), ForeignKey("clients.id"), nullable=False
    )
    client = relationship("DBClient", back_populates="projects")
    activities = relationship("DBActivity", back_populates="project")


class DBActivity(BaseModel):
    __tablename__ = "activities"

    id: Mapped[uuid.UUID] = mapped_column(
        postgresql.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=True)
    project_id: Mapped[uuid.UUID] = mapped_column(
        postgresql.UUID(as_uuid=True), ForeignKey("projects.id"), nullable=False
    )
    project = relationship("DBProject", back_populates="activities")
