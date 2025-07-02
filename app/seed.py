from app.core.db_connect import SessionLocal
from app.model.account_model import Account
from app.utils.jwt_util import hash_password

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
        from app.model.exam_model import Subject
        subjects = [
            Subject(name="Python cho kỹ sư", subject_code="PPR501"),
            Subject(name="Xử lý tín hiệu số", subject_code="DSP501")
        ]
        db.add_all(subjects)
        db.commit()
        print("Seeded subjects.")
    finally:
        db.close()
if __name__ == "__main__":
    seed_accounts()
    seed_subject()
