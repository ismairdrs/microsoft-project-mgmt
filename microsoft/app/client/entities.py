from pydantic import BaseModel


class ClientIn(BaseModel):
    name: str
    email: str
    phone: str | None = None
