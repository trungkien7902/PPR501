from http import HTTPStatus
from app.model.models import Account
from app.core.db_connect import SessionLocal
from app.utils.jwt_util import verify_password, create_access_token, create_refresh_token
from sqlalchemy.orm import Session
from app.schema.schema import AuthRequest, TokenResponse
from app.core.app_config import CustomException


def login(auth_request: AuthRequest) -> TokenResponse:
    db: Session = SessionLocal()
    try:
        if not auth_request.username:
            raise CustomException(
                "Tên đăng nhập không được để trống.",
                HTTPStatus.BAD_REQUEST
            )

        if not auth_request.password:
            raise CustomException(
                "Mật khẩu không được để trống.",
                HTTPStatus.BAD_REQUEST
            )

        user = (
            db.query(Account)
            .filter(Account.username == auth_request.username)
            .first()
        )

        if not user:
            raise CustomException(
                "Tài khoản không tồn tại.",
                HTTPStatus.NOT_FOUND
            )

        if not verify_password(auth_request.password, str(user.hashed_password)):
            raise CustomException(
                "Mật khẩu không chính xác.",
                HTTPStatus.UNAUTHORIZED
            )

        token_data = {
            "sub": user.username,
            "role": user.role,
            "user_id": user.id
        }

        response = TokenResponse(
            access_token=create_access_token(token_data),
            refresh_token=create_refresh_token(token_data)
        )

        return response
    except CustomException:
        raise
    except Exception as e:
        raise CustomException(
            f"Đã xảy ra lỗi hệ thống khi đăng nhập: {str(e)}",
            HTTPStatus.INTERNAL_SERVER_ERROR
        )
    finally:
        db.close()
