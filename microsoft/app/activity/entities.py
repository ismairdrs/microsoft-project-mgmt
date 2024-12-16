from uuid import UUID

from pydantic import BaseModel


class ActivityIn(BaseModel):
    name: str
    description: str | None = None
    project_id: UUID
