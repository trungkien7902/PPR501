from http import HTTPStatus

from fastapi import APIRouter
from fastapi.responses import JSONResponse
from typing import List

from app.schema.schema import ExamResponse, IResponseBase, SubmitExamRequest, SubmitExamResponse
from app.service.exam_service import get_exam_by_subject_code, get_exam_by_exam_code, update_exam_by_exam_code, submit

exam_route = APIRouter()

@exam_route.get("/{subject_code}", response_model=List[ExamResponse])
def get_exams_of_subject(subject_code: str):
    response = get_exam_by_subject_code(subject_code)
    return JSONResponse(
        status_code=HTTPStatus.OK,
        content=IResponseBase[List[ExamResponse]](
            code=HTTPStatus.OK,
            message="Lấy danh sách bài kiểm tra thành công.",
            items=response
        ).model_dump()
    )

@exam_route.get("/exam/{exam_code}", response_model=ExamResponse)
def get_exam_detail(exam_code: str):
    response = get_exam_by_exam_code(exam_code)
    return JSONResponse(
        status_code=HTTPStatus.OK,
        content=IResponseBase[ExamResponse](
            code=HTTPStatus.OK,
            message="Lấy thông tin bài kiểm tra thành công.",
            items=response
        ).model_dump()
    )

@exam_route.put("/exam/{exam_code}",response_model=ExamResponse)
def update_exam( newExam: ExamResponse):
    updated_exam = update_exam_by_exam_code(newExam)
    return JSONResponse(
        status_code=HTTPStatus.OK,
        content=IResponseBase[ExamResponse](
            code=HTTPStatus.OK,
            message="Cập nhật bài kiểm tra thành công.",
            items=updated_exam
        ).model_dump()
    )

@exam_route.post("/exam/submit")
def submit_exam(request: SubmitExamRequest):
    response = submit(request)
    return JSONResponse(
        status_code=HTTPStatus.OK,
        content=IResponseBase[SubmitExamResponse](
            code=HTTPStatus.OK,
            message="Nộp bài kiểm tra thành công.",
            items=response
        ).model_dump()
    )