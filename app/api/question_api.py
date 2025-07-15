from http import HTTPStatus
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from app.schema.schema import IResponseBase, QuestionResponse
from typing import List

from app.service.question_service import get_questions_by_exam_id

question_route = APIRouter()


@question_route.get("/question/{exam_id}")
def get_questions_by_exam_id(exam_id: str):
    response = get_questions_by_exam_id(exam_id)
    return JSONResponse(
        status_code=HTTPStatus.OK,
        content=IResponseBase[List[QuestionResponse]](
            status=HTTPStatus.OK,
            message=f"Lấy danh sách câu hỏi của bài kiểm tra với id là {exam_id} thành công.",
            items=response
        ).model_dump()
    )
