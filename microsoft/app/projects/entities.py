from uuid import UUID

from pydantic import BaseModel

from microsoft.enums import ProjectStatus


class ProjectIn(BaseModel):
    name: str
    status: ProjectStatus
    client_id: UUID
    description: str | None = None
