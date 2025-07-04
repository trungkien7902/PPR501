from contextvars import ContextVar

auth_context: ContextVar[dict] = ContextVar("auth_context", default={})

def set_auth_context(data: dict):
    auth_context.set(data)

def get_auth_context() -> dict:
    return auth_context.get()