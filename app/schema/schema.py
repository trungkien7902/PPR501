from typing import Generic, TypeVar, List
from pydantic import BaseModel, constr, ConfigDict

T = TypeVar("T")


class IResponseBase(BaseModel, Generic[T]):
    code: int = 100
    message: str = "Success"
    items: T | None = None


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
class QuestionOptionSchema(BaseModel):
    option_text: str
    is_correct: bool

    model_config = ConfigDict(from_attributes=True)

class ExamQuestionSchema(BaseModel):
    question_text: str
    options: List[QuestionOptionSchema]

    model_config = ConfigDict(from_attributes=True)

class CreateExamSchema(BaseModel):
    subject_id: int
    valid_date: str
    start_time: str
    duration: int
    question: List[ExamQuestionSchema]

    model_config = ConfigDict(from_attributes=True)
