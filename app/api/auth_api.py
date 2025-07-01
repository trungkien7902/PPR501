from http import HTTPStatus

from app.service.auth_service import login
from fastapi import HTTPException, APIRouter
from fastapi.responses import JSONResponse
from app.schema.schema import AuthRequest, TokenResponse, IResponseBase

auth_router = APIRouter()

@auth_router.post("/login")
def login_user(auth_request: AuthRequest):
    response = login(auth_request)
    if not response:
        return JSONResponse(
            status_code=HTTPStatus.UNAUTHORIZED,
            content=IResponseBase[None](
                code=HTTPStatus.UNAUTHORIZED,
                message="Tên đăng nhập hoặc mật khẩu không đúng",
            ).model_dump()
        )
    return JSONResponse(
        status_code=HTTPStatus.OK,
        content=IResponseBase[TokenResponse](
            code=HTTPStatus.OK,
            message="Đăng nhập thành công",
            items=response
        ).model_dump()
    )


@auth_router.get("/logout")
def logout_user():
    # TODO: Implement logout functionality
    return {"message": "Logout endpoint is not implemented yet."}
