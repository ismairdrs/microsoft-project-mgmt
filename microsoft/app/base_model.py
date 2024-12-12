import uuid
from datetime import datetime

from sqlalchemy import DateTime
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import Mapped, mapped_column

from gringotts.db import Base
from gringotts.db.functions import utcnow


class BaseModel(Base):
    __abstract__ = True

    id: Mapped[uuid.UUID] = mapped_column(
        postgresql.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=utcnow()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=utcnow(),
        onupdate=utcnow(),
    )
