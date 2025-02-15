from fastapi import FastAPI
from routes.v1.router import v1_router

app = FastAPI(
    title="UK Government Contact Book API",
    description="API for the UK Government Contact Book",
    version="1.0.0",
    docs_url="/",
)

app.include_router(v1_router, prefix="/api")
