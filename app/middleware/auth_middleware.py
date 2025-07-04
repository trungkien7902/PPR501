from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.auth_context import set_auth_context
from app.utils.jwt_util import decode_access_token

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
            payload = decode_access_token(token)
            if payload:
                set_auth_context(payload)

        response = await call_next(request)
        return response
