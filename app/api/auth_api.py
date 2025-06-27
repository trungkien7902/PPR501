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
        return JSONResponse(status_code=HTTPStatus.UNAUTHORIZED,
                            content=IResponseBase[None](
                                code=HTTPStatus.UNAUTHORIZED,
                                message="Invalid username or password")
                            )
    return JSONResponse(
        status_code=HTTPStatus.OK,
        content=IResponseBase[TokenResponse](
            code=HTTPStatus.OK,
            message="Login successful",
            items=response
        )
    )


@auth_router.get("/logout")
def logout_user():
    # TODO: Implement logout functionality
    return {"message": "Logout endpoint is not implemented yet."}
