from http import HTTPStatus
from typing import List
from app.model.models import Subject, SubjectAssign
from app.schema.schema import CustomException, SubjectResponse
from app.core.db_connect import SessionLocal

db = SessionLocal()


def get_subjects(account_id: int) -> List[SubjectResponse]:
    try:
        subjects = (
            db.query(Subject)
            .join(SubjectAssign, Subject.id == SubjectAssign.subject_id)
            .filter(SubjectAssign.account_id == account_id)
            .all()
        )

        if not subjects:
            raise CustomException("Không tìm thấy môn học nào được gán cho tài khoản.", HTTPStatus.NOT_FOUND)

        return [SubjectResponse.from_orm(subject) for subject in subjects]

    except Exception as e:
        db.rollback()
        raise CustomException(f"Lỗi khi lấy danh sách môn học: {str(e)}", HTTPStatus.INTERNAL_SERVER_ERROR)
    finally:
        db.close()
