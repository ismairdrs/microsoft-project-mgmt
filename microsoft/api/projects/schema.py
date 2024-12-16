from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from microsoft.enums import ProjectStatus


class ProjectIn(BaseModel):
    name: str = Field(
        title="Project Name",
        description="Name of the project",
        examples=["New Website Development"],
    )
    description: str | None = Field(
        title="Description",
        description="Detailed description of the project",
        examples=["Develop a responsive website for the client"],
    )
    client_id: UUID = Field(
        title="Client ID",
        description="ID of the client associated with the project",
        examples=["2740411e-1ca8-4d2c-9bc3-2e6eaef6c0ca"],
    )


class ProjectOut(BaseModel):
    id: UUID = Field(
        title="Project ID",
        description="ID of the project",
        examples=["5b2c6d4e-aef0-11ec-b909-0242ac120002"],
    )
    name: str = Field(
        title="Project Name",
        description="Name of the project",
        examples=["New Website Development"],
    )
    description: str | None = Field(
        title="Description",
        description="Detailed description of the project",
        examples=["Develop a responsive website for the client"],
    )
    status: ProjectStatus = Field(
        title="Project Status",
        description="Status of the project",
        examples=["open", "in_progress", "closed"],
    )
    client_id: UUID = Field(
        title="Client ID",
        description="ID of the client associated with the project",
        examples=["2740411e-1ca8-4d2c-9bc3-2e6eaef6c0ca"],
    )
    created_at: datetime = Field(
        ...,
        title="Created at",
        examples=["2020-01-01 00:00:00"],
    )
