from http import HTTPStatus

from fastapi import APIRouter, UploadFile, File, HTTPException
import tempfile
import shutil
from fastapi.responses import JSONResponse

from app.model.exam_model import ExamQuestion
from app.schema.schema import IResponseBase, ExamQuestionSchema
from app.service.file_service import parse_questions_from_docx

file_route = APIRouter()

@file_route.post("/import")
async def preview_questions_from_docx(
        file: UploadFile = File(...)
):
    if not file.filename.endswith(".docx"):
        raise HTTPException(status_code=500, detail="Chỉ hỗ trợ định dạng .docx")

    with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp:
        shutil.copyfileobj(file.file, tmp)
        tmp_path = tmp.name

    try:
        questions_data = parse_questions_from_docx(tmp_path)
        questions_schema = [ExamQuestionSchema.model_validate(q) for q in questions_data]
        return JSONResponse(
            status_code=HTTPStatus.OK,
            content=IResponseBase[list[ExamQuestionSchema]](
                code=HTTPStatus.OK,
                message="Import thành công",
                items=questions_schema
            ).model_dump(mode="json")
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi xử lý file: {str(e)}")