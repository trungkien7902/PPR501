from http import HTTPStatus

from app.service.auth_service import login
from fastapi import APIRouter, Body
from fastapi.responses import JSONResponse
from app.schema.schema import AuthRequest, TokenResponse, IResponseBase, CustomException
from typing import Any

auth_router = APIRouter()


@auth_router.post("/login")
def login_user(auth_request: AuthRequest):
    response = login(auth_request)
    if not response:
        return JSONResponse(
            status_code=HTTPStatus.UNAUTHORIZED,
            content=IResponseBase[Any](
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

@auth_router.post("/refresh", response_model=IResponseBase[TokenResponse])
def refresh_access_token(refresh_token: str = Body(...)):
    from app.utils.jwt_util import decode_access_token, create_access_token

    payload = decode_access_token(refresh_token)
    if not payload:
        raise CustomException(status_code=HTTPStatus.UNAUTHORIZED, message="Refresh token không hợp lệ hoặc đã hết hạn")

    if payload.get("type") != "refresh":
        raise CustomException(status_code=HTTPStatus.BAD_REQUEST, message="Không phải là refresh token")

    new_access_token = create_access_token({
        "sub": payload.get("sub"),
        "role": payload.get("role"),
        "user_id": payload.get("user_id")
    })

    return IResponseBase[TokenResponse](
        code=HTTPStatus.OK,
        message="Làm mới access token thành công",
        items=TokenResponse(
            access_token=new_access_token,
            refresh_token=refresh_token
        )
    )
@auth_router.get("/logout")
def logout_user():
    # TODO: Implement logout functionality
    return {"message": "Logout endpoint is not implemented yet."}
