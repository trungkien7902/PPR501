from fastapi import APIRouter

from app.schema.schema import CreateExamSchema

exam_route = APIRouter()

@exam_route.post("/")
async def create_exam(create_exam_schema: CreateExamSchema):
    # TODO: Implement the logic to create an exam.
    return None
