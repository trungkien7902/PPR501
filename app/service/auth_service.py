from app.model.account_model import Account
from app.core.db_connect import SessionLocal
from app.utils.jwt_util import verify_password, create_access_token
from sqlalchemy.orm import Session

def login(username: str, password: str) -> str:
    db: Session = SessionLocal()
    try:
        user = (db.query(Account)
                .filter(Account.username == username)
                .first())
        if not user or not verify_password(password, user.hashed_password):
            return None
        token_data = {
            "sub": user.username,
            "role": user.role,
            "user_id": user.id
        }
        return create_access_token(token_data)
    finally:
        db.close()

