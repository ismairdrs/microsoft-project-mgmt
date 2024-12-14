from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field


class ClientIn(BaseModel):
    name: str = Field(
        title="Name",
        description="Name",
        examples=["Ismair Junior"],
    )
    email: str = Field(
        title="e-mail",
        description="E-mail contact",
        examples=["test@gmail.com"],
    )
    phone: str = Field(
        title="Phone",
        description="Phone Number",
        examples=["62981888888"],
    )


class ClientOut(BaseModel):
    id: UUID = Field(
        title="Client ID",
        description="Identification of the Client ID",
        examples=["2740411e-1ca8-4d2c-9bc3-2e6eaef6c0ca"],
    )
    name: str = Field(
        title="Name",
        description="Name",
        examples=["Ismair Junior"],
    )
    email: str = Field(
        title="e-mail",
        description="E-mail contact",
        examples=["test@gmail.com"],
    )
    phone: str = Field(
        title="Phone",
        description="Phone Number",
        examples=["62981888888"],
    )
    created_at: datetime = Field(
        ...,
        title="Created at",
        examples=["2020-01-01 00:00:00"],
    )
    updated_at: datetime = Field(
        ...,
        title="Updated at",
        examples=["2020-01-01 00:00:00"],
    )
