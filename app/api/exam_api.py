from http import HTTPStatus

from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from app.service.exam_service import parse_full_exam, save_exam
from app.schema.schema import ExamPreview, IResponseBase
from typing import Any
import os
import tempfile

exam_route = APIRouter()


@exam_route.post("")
async def save(exam_request: ExamPreview):
    response = save_exam(exam_request)
    return JSONResponse(
        status_code=HTTPStatus.OK,
        content=IResponseBase[int](
            code=HTTPStatus.OK,
            message="API exam is running",
            items=response
        ).model_dump()
    )


@exam_route.post("/import", response_model=ExamPreview)
async def preview_exam(file: UploadFile = File(...)):
    if not file.filename.endswith(".docx"):
        raise HTTPException(status_code=400, detail="Chỉ hỗ trợ file .docx")

    tmp_path = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp:
            tmp.write(await file.read())
            tmp_path = tmp.name
        exam = parse_full_exam(tmp_path)
        return JSONResponse(
            status_code=HTTPStatus.OK,
            content=IResponseBase[ExamPreview](
                code=HTTPStatus.OK,
                message="Tải file thành công",
                items=exam
            ).model_dump()
        )
    except Exception as e:
        return JSONResponse(
            status_code=HTTPStatus.BAD_REQUEST,
            content=IResponseBase[Any](
                code=HTTPStatus.BAD_REQUEST,
                message=f"Có lỗi xảy ra khi xử lý file: {str(e)}",
                items=None
            ).model_dump()
        )
    finally:
        if tmp_path and os.path.exists(tmp_path):
            os.remove(tmp_path)
