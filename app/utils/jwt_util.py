from http import HTTPStatus

import jwt
from datetime import datetime, timedelta
from app.core.config import JWT_SECRET_KEY, JWT_ALGORITHM, JWT_EXP_DELTA_SECONDS
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.schema.schema import CustomException

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

# hashing
def hash_password(password: str) -> str:
    return jwt.encode({"password": password}, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        decoded = jwt.decode(hashed_password, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return decoded.get("password") == plain_password
    except jwt.InvalidTokenError:
        return False


# Create JWT token
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(seconds=JWT_EXP_DELTA_SECONDS)
    to_encode.update({
        "exp": expire,
        "type": "access"
    })
    return jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)


def create_refresh_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=30)
    to_encode.update({
        "exp": expire,
        "type": "refresh"
    })
    return jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)


# Decode JWT token
def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise CustomException(
            "Token hết hạn sử dụng",
            HTTPStatus.UNAUTHORIZED
        )
    except jwt.InvalidTokenError:
        raise CustomException(
            "Token không hợp lệ",
            HTTPStatus.UNAUTHORIZED
        )

def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return payload