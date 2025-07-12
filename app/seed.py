from app.core.db_connect import SessionLocal
from app.model.models import Account, Subject, SubjectAssign, ExamAssign, Exam
from app.utils.jwt_util import hash_password
import random
def seed_accounts():
    db = SessionLocal()
    try:
        accounts = [
            Account(
                username="admin",
                email="admin@example.com",
                hashed_password=hash_password("123456"),
                role="ADMIN"
            ),
            Account(
                username="staff1",
                email="staff1@example.com",
                hashed_password=hash_password("123456"),
                role="STAFF"
            ),
            Account(
                username="staff2",
                email="staff2@example.com",
                hashed_password=hash_password("123456"),
                role="STAFF"
            ),
        ]
        # Add 7 students
        for i in range(1, 8):
            accounts.append(
                Account(
                    username=f"student{i}",
                    email=f"student{i}@example.com",
                    hashed_password=hash_password("123456"),
                    role="STUDENT"
                )
            )
        db.add_all(accounts)
        db.commit()
        print("Seeded 1 admin, 2 staff, 7 student accounts.")
    finally:
        db.close()

def seed_subject():
    db = SessionLocal()
    try:
        subjects = [
            Subject(name="Python cho kỹ sư", subject_code="PPR501"),
            Subject(name="Xử lý tín hiệu số", subject_code="DSP501"),
            Subject(name="Cơ sở dữ liệu", subject_code="DBI101"),
            Subject(name="Trí tuệ nhân tạo", subject_code="AI601"),
            Subject(name="Nhập môn mạng máy tính", subject_code="NET101"),
            Subject(name="Hệ điều hành", subject_code="OS202"),
            Subject(name="Kiến trúc máy tính", subject_code="CAO201"),
            Subject(name="Cấu trúc dữ liệu và giải thuật", subject_code="DSA301"),
        ]
        db.add_all(subjects)
        db.commit()
        print("Seeded subjects.")
    finally:
        db.close()

def seed_subject_assign():
    db = SessionLocal()
    try:
        subjects = db.query(Subject).all()
        accounts = db.query(Account).filter(Account.role == "STAFF").all()
        if not subjects or not accounts:
            print("No subjects or staff accounts to assign.")
            return

        assignments = []
        for subject in subjects:
            staff = random.choice(accounts)
            assignments.append(
                SubjectAssign(
                    subject_id=subject.id,
                    account_id=staff.id
                )
            )
        db.add_all(assignments)
        db.commit()
        print("Seeded subject assignments.")
    finally:
        db.close()

def seed_exam_assign():
    db = SessionLocal()
    try:
        exams = db.query(Exam).all()
        accounts = db.query(Account).filter(Account.role == "STAFF").all()
        if not exams or not accounts:
            print("No subjects or student to assign.")
            return

        assignments = []
        for exam in exams:
            student = random.choice(accounts)
            assignments.append(
                ExamAssign(
                    exam_id=exam.id,
                    account_id=student.id
                )
            )
        db.add_all(assignments)
        db.commit()
        print("Seeded subject assignments.")
    finally:
        db.close()
if __name__ == "__main__":
    # seed_accounts()
    # seed_subject()
    # seed_subject_assign()
    seed_exam_assign()