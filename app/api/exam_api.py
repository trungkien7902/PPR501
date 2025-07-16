from http import HTTPStatus
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from app.schema.schema import IResponseBase, ExamResponse, QuestionResponse, TakeExamRequest
from app.service.exam_service import get_exam_by_subject_code
from app.service.question_service import submit_exam
from typing import List

exam_route = APIRouter()


@exam_route.get("/exam/{subject_code}")
def get_exam(subject_code: str):
    response = get_exam_by_subject_code(subject_code)
    return JSONResponse(
        status_code=HTTPStatus.OK,
        content=IResponseBase[List[ExamResponse]](
            status=HTTPStatus.OK,
            message=f"Lấy danh sách bài kiểm tra môn {subject_code} thành công.",
            items=response
        ).model_dump()
    )


@exam_route.post("/exams/take_")
def take_exam(request: TakeExamRequest):
    response = take_exam(request)
    return JSONResponse(
        status_code=HTTPStatus.OK,
        content=IResponseBase[ExamResponse](
            status=HTTPStatus.OK,
            message="Lấy thông tin bài kiểm tra thành công.",
            items=response
        ).model_dump()
    )


@exam_route.post("/exam_submit")
def submit_exam_api(answers: List[QuestionResponse], exam_id: int, student_id: int):
    response = submit_exam(answers, exam_id, student_id)
    return JSONResponse(
        status_code=HTTPStatus.OK,
        content=IResponseBase[List[ExamResponse]](
            status=HTTPStatus.OK,
            message=response,
            items=response
        ).model_dump()
    )
