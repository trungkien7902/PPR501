from typing import Optional
from app.model.models import Account
from app.core.db_connect import SessionLocal
from app.utils.jwt_util import verify_password, create_access_token, create_refresh_token
from sqlalchemy.orm import Session

from app.schema.schema import AuthRequest, TokenResponse


def login(auth_request: AuthRequest) -> Optional[TokenResponse]:
    db: Session = SessionLocal()
    try:
        user = (
            db.query(Account)
            .filter(Account.username == auth_request.username)
            .first()
        )
        if not user or not verify_password(auth_request.password, user.hashed_password):
            return None
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
    finally:
        db.close()