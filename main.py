from app.api import auth_api, exam_api

from app.core.app_config import app

app.include_router(auth_api.auth_router, prefix="/auth")
app.include_router(exam_api.exam_route, prefix="/exam")
