from sqlalchemy import Column, Integer, String, CheckConstraint

from app.model.base import Base


class Account(Base):
    __tablename__ = "accounts"
    __table_args__ = (
        CheckConstraint(
            "role IN ('STAFF', 'ADMIN', 'STUDENT')",
            name="check_role_valid_values"
        ),
    )

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(50), default="STUDENT", nullable=False, index=True)
