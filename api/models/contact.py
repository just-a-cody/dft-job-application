from pydantic import BaseModel


class ContactModel(BaseModel):
    id: int
    name: str
    email: str
    phone: str
    address: str
