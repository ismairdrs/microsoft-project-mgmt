from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class ActivityIn(BaseModel):
    name: str = Field(
        title="Activity Name",
        description="Name of the activity",
        examples=["Design Homepage"],
    )
    description: str | None = Field(
        title="Description",
        description="Detailed description of the activity",
        examples=["Create the homepage layout with Figma"],
    )
    project_id: UUID = Field(
        title="Project ID",
        description="ID of the project associated with the activity",
        examples=["5b2c6d4e-aef0-11ec-b909-0242ac120002"],
    )


class ActivityOut(BaseModel):
    id: UUID = Field(
        title="Activity ID",
        description="ID of the activity",
        examples=["74d1a60c-aef0-11ec-b909-0242ac120002"],
    )
    name: str = Field(
        title="Activity Name",
        description="Name of the activity",
        examples=["Design Homepage"],
    )
    description: str | None = Field(
        title="Description",
        description="Detailed description of the activity",
        examples=["Create the homepage layout with Figma"],
    )
    project_id: UUID = Field(
        title="Project ID",
        description="ID of the project associated with the activity",
        examples=["5b2c6d4e-aef0-11ec-b909-0242ac120002"],
    )
    created_at: datetime = Field(
        ...,
        title="Created at",
        examples=["2020-01-01 00:00:00"],
    )
