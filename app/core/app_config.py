from fastapi import FastAPI, Request
from app.api import auth_api, exam_api
from fastapi.responses import JSONResponse
from http import HTTPStatus
from typing import Any

from app.schema.schema import IResponseBase

# App define
app = FastAPI(
    title="PPR501",
    description="API documentation ",
    version="1.0.0",
    docs_url="/docs",
)


# Exception handler
class CustomException(Exception):
    def __init__(self, message: str = "Có lỗi xảy ra", status_code: int = HTTPStatus.INTERNAL_SERVER_ERROR):
        self.message = message
        self.status_code = status_code


@app.exception_handler(CustomException)
async def custom_exception_handler(request: Request, exc: CustomException) -> JSONResponse:
    response_data = IResponseBase(
        code=exc.status_code,
        message=exc.message,
        items=f"URL: {request.url.path}, Method: {request.method}"
    )
    return JSONResponse(
        status_code=exc.status_code,
        content=response_data.model_dump()
    )
