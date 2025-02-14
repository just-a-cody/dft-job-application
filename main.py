from fastapi import FastAPI
from routes import contacts
app = FastAPI(
    title="FastAPI Boilerplate",
    description="A boilerplate for FastAPI",
    version="0.1.0",
    docs_url="/",
)

app.include_router(contacts.router)