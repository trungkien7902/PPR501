from http import HTTPStatus

from fastapi import APIRouter
from fastapi.responses import JSONResponse
from typing import List

from app.service.subject_service import get_subjects
from app.schema.schema import SubjectResponse, CustomException, IResponseBase
from app.core.auth_context import get_auth_context

subject_route = APIRouter()


@subject_route.get("", response_model=List[SubjectResponse])
def get_subjects_by_account():
    auth_context = get_auth_context()
    account_id = auth_context.get("user_id")

    if not account_id:
        raise CustomException("Không xác định được tài khoản.", 401)

    subjects = get_subjects(account_id)
    return JSONResponse(
        status_code=HTTPStatus.OK,
        content=IResponseBase[List[SubjectResponse]](
            status=HTTPStatus.OK,
            message="Lấy danh sách môn học thành công.",
            items=subjects
        ).model_dump()
    )
