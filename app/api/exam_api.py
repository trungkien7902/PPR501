from http import HTTPStatus
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from app.schema.schema import IResponseBase, ExamResponse
from app.service.exam_service import get_exam_by_subject_code
from typing import List

exam_route = APIRouter()


@exam_route.get("/exam/{subject_code}")
def get_exam(exam_code: str):
    response = get_exam_by_subject_code(exam_code)
    return JSONResponse(status_code=HTTPStatus.OK,
                        content=IResponseBase[List[ExamResponse]](
                            status=HTTPStatus.OK,
                            message="Lấy danh sách bài kiểm tra thành công.",
                            items=response
                        ).model_dump())
