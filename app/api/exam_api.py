from fastapi import APIRouter, UploadFile, File, HTTPException
from app.service.exam_service import parse_full_exam
from app.schema.schema import ExamPreview
import os
import tempfile

exam_route = APIRouter()

@exam_route.post("/exam/preview", response_model=ExamPreview)
async def preview_exam(file: UploadFile = File(...)):
    if not file.filename.endswith(".docx"):
        raise HTTPException(status_code=400, detail="Only .docx files are supported")
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp:
            tmp.write(await file.read())
            tmp_path = tmp.name
        exam = parse_full_exam(tmp_path)
        return exam
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)