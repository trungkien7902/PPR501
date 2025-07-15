from http import HTTPStatus
from typing import List
from app.model.models import Subject
from app.schema.schema import CustomException, ExamResponse
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
