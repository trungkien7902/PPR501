from http import HTTPStatus
from typing import Generic, TypeVar, List, Optional
from pydantic import BaseModel, constr

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
class Options(BaseModel):
    content: str
    is_correct: bool


class QuestionChoiceResponse(BaseModel):
    question_id: int = None
    content: Optional[str] = None
    id: int = None


class QuestionResponse(BaseModel):
    content: Optional[str] = None
    file_id: Optional[str] = None
    mark: float = 1.0
    unit: Optional[str] = None
    mix_choices: bool = False
    options: List[Options] = []
    selectedChoice: int = None
    questionChoices: List[QuestionChoiceResponse] = []
    exam_id: int = None
    id: int = None


class ExamResponse(BaseModel):
    name: str
    subject_code: str
    number_quiz: int
    valid_from: str
    valid_to: str
    duration_minutes: int
    description: str
    questions: List[QuestionResponse]
    id: int


# Subject Service Schema
class SubjectResponse(BaseModel):
    name: str
    subject_code: str