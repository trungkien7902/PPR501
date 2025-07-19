from typing import List
from http import HTTPStatus
from app.model.models import Subject, SubjectAssign
from app.schema.schema import CustomException, SubjectResponse
from app.core.db_connect import SessionLocal

def get_subjects(account_id: int) -> List[SubjectResponse]:
    db = SessionLocal()
    try:
        subjects = (
            db.query(Subject)
            .join(SubjectAssign, Subject.id == SubjectAssign.subject_id)
            .filter(SubjectAssign.account_id == account_id)
            .all()
        )

        if not subjects:
            raise CustomException("Không tìm thấy môn học nào được gán cho tài khoản.", HTTPStatus.NOT_FOUND)

        subject_responses = [
            SubjectResponse(
                id=subject.id,
                name=subject.name,
                subject_code=subject.subject_code
            ) for subject in subjects
        ]
        return subject_responses

    except Exception as e:
        # Không cần rollback nếu chỉ đọc dữ liệu
        raise CustomException(f"Lỗi khi lấy danh sách môn học: {str(e)}", HTTPStatus.INTERNAL_SERVER_ERROR)
    finally:
        db.close()
