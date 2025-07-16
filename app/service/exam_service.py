from http import HTTPStatus
from typing import List
from app.model.models import Subject, SubjectAssign, ExamQuestion
from app.schema.schema import CustomException, ExamResponse, ExamUpdateRequest, Options
from app.model.models import Exam
from app.core.db_connect import SessionLocal

db = SessionLocal()


def get_exam_by_subject_code(subject_code: str) -> List[ExamResponse]:
    try:
        subject = db.query(Subject).filter(Subject.subject_code == subject_code).first()
        if not subject:
            raise CustomException(f"Môn học với mã {subject_code} không tồn tại.", HTTPStatus.NOT_FOUND)
        exams = db.query(Exam).filter(Exam.subject_id == subject.id).all()
        if not exams:
            raise CustomException(f"Không tìm thấy bài kiểm tra nào cho môn học {subject_code}.", HTTPStatus.NOT_FOUND)
        exam_responses = []
        for exam in exams:
            exam_responses.append(ExamResponse(
                id=exam.id,
                name=exam.name,
                subject_code=subject.subject_code,
                number_quiz=exam.number_quiz,
                valid_from=exam.valid_from.isoformat(),
                valid_to=exam.valid_to.isoformat(),
                duration_minutes=exam.duration_minutes,
                description=exam.description,
                questions=[]
            ))

        return exam_responses
    except CustomException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        raise CustomException(f"Đã xảy ra lỗi hệ thống: {str(e)}", HTTPStatus.INTERNAL_SERVER_ERROR)
    finally:
        db.close()

# Update exam
def update_exam(request: ExamUpdateRequest) -> None:
    try:
        exam = db.query(Exam).filter(Exam.exam_code == request.exam_code).first()
        if not exam:
            raise CustomException(f"Bài kiểm tra với mã {request.exam_code} không tồn tại.", HTTPStatus.NOT_FOUND)

        # Check assignments
        subject = exam.subject
        assignments = db.query(SubjectAssign).filter(SubjectAssign.subject_id == subject.id).all()

        if not any(assignment.account_id == request.account_id for assignment in assignments):
            raise CustomException(f"Bạn không có quyền cập nhật bài kiểm tra cho môn học {subject.name}.",
                                  HTTPStatus.FORBIDDEN)

        # Update exam logic:
        exam.name = request.name
        exam.number_quiz = request.number_quiz
        exam.valid_from = request.valid_from
        exam.valid_to = request.valid_to
        exam.duration_minutes = request.duration_minutes
        exam.description = request.description
        # Clear existing questions and add new ones
        exam.questions.clear()
        for question in request.questions:
            new_question = ExamQuestion(
                content=question.content,
                file_id=question.file_id,
                mark=question.mark,
                unit=question.unit,
                mix_choices=question.mix_choices
            )
            for option in question.options:
                new_option = Options(
                    content=option.content,
                    is_correct=option.is_correct
                )
                new_question.options.append(new_option)
            exam.questions.append(new_question)
        db.add(exam)
        db.commit()
    except CustomException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        raise CustomException(f"Đã xảy ra lỗi hệ thống: {str(e)}", HTTPStatus.INTERNAL_SERVER_ERROR)
    finally:
        db.close()
