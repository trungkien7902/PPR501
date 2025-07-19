from http import HTTPStatus
from typing import Generic, TypeVar, List, Optional
from pydantic import BaseModel, constr

T = TypeVar("T")


class IResponseBase(BaseModel, Generic[T]):
    code: int = 200
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

class Options(BaseModel):
    id: int
    question_id: int
    content: str
    is_correct: bool | None = None  # Optional for non-admin users

class QuestionResponse(BaseModel):
    id: int
    content: str
    file_id: str | None = None
    mark: float
    unit: str
    mix_choices: bool
    options: List['Options'] = []

# Exam Response
class ExamResponse(BaseModel):
    id: int
    name: str
    subject_code: str
    number_quiz: int
    valid_from: str  # ISO format date string
    valid_to: str  # ISO format date string
    duration_minutes: int
    description: Optional[str] = None
    questions: List['QuestionResponse'] = []

# Get list of subjects
class SubjectResponse(BaseModel):
    id: int
    name: str
    subject_code: str

class TakeExamRequest(BaseModel):
    exam_code: str
    username: str
    password: str

class AnswerItem(BaseModel):
    question_id: int
    option_id: int

class SubmitExamRequest(BaseModel):
    username: str
    exam_code: str
    answers: List[AnswerItem]

class SubmitExamResponse(BaseModel):
    exam_code: str
    score: float
    total_questions: int
    correct_answers: int
    incorrect_answers: int