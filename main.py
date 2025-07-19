from starlette.middleware.cors import CORSMiddleware

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.api import auth_api, subject_api, exam_api
from app.middleware.auth_middleware import AuthMiddleware
from app.schema.schema import IResponseBase, CustomException

app = FastAPI(
    title="PPR501",
    description="API documentation ",
    version="1.0.0",
    docs_url="/docs",
)
app.add_middleware(AuthMiddleware)


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


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(auth_api.auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(subject_api.subject_route, prefix="/subjects", tags=["Subjects"])

app.include_router(exam_api.exam_route, prefix="/exams", tags=["Exams"])