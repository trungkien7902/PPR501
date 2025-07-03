from fastapi import FastAPI
from app.api import auth_api, exam_api

app = FastAPI(
    title="PPR501",
    description="API documentation ",
    version="1.0.0",
    docs_url="/docs",
)
app.include_router(auth_api.auth_router, prefix="/auth")
app.include_router(exam_api.exam_route, prefix="/exam")
