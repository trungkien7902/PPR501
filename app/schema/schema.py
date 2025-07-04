from http import HTTPStatus
from typing import Generic, TypeVar, List, Optional
from pydantic import BaseModel, constr, ConfigDict

T = TypeVar("T")


class IResponseBase(BaseModel, Generic[T]):
    code: int = 100
    message: str = "Success"
    items: T | None = None


# Exception handler
class CustomException(Exception):
    def __init__(self, message: str = "Có lỗi xảy ra", status_code: int = HTTPStatus.INTERNAL_SERVER_ERROR):
        self.message = message
        self.status_code = status_code


# Auth Service Schema
## Request
class AuthRequest(BaseModel):
    username: str
    password: constr(min_length=5)


## Response
class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str


# Exam Service Schema
class QuestionChoice(BaseModel):
    content: str
    is_correct: bool = False


class QuestionPreview(BaseModel):
    content: Optional[str] = None
    file_id: Optional[str] = None
    mark: float = 1.0
    unit: Optional[str] = None
    mix_choices: bool = False
    options: List[QuestionChoice] = []


class ExamPreview(BaseModel):
    name: Optional[str] = None
    subject_id: Optional[str] = None
    number_quiz: Optional[int] = 0
    start_date: Optional[str] = None
    duration_minutes: Optional[int] = 0
    description: Optional[str] = None
    is_active: Optional[bool] = True
    questions: List[QuestionPreview] = []
