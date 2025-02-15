from pydantic import BaseModel


class ContactModel(BaseModel):
    id: str
    name: str
    email: str
    phone: str
    address: str
