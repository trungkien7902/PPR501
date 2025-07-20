from http import HTTPStatus

from fastapi import APIRouter, UploadFile, File, FastAPI
from fastapi.responses import JSONResponse
from typing import List
import os

from fastapi.staticfiles import StaticFiles

from app.schema.schema import ExamResponse, IResponseBase, SubmitExamRequest, SubmitExamResponse
from app.service.exam_service import get_exam_by_subject_code, get_exam_by_exam_code, update_exam_by_exam_code, submit
from uuid import uuid4

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

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
exam_route.mount("/uploads", StaticFiles(directory="uploads"), name="images")

@exam_route.post("/files/upload",response_model=str)
async def upload_question_file(file: UploadFile = File(...)):
    ext = os.path.splitext(file.filename)[1]
    file_id = f"{uuid4().hex}{ext}"
    file_path = os.path.join(UPLOAD_FOLDER, file_id)
    with open(file_path, "wb") as f:
        print(1)
        f.write(await file.read())
    return JSONResponse(content={"file_id": file_id})

