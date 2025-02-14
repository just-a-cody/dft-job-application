from fastapi import APIRouter
from api.routes.v1.endpoints import contacts

v1_router = APIRouter(
    prefix="/v1",
)

v1_router.include_router(contacts.router, prefix="/contacts")
