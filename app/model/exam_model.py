from sqlalchemy import Column, Integer, String, CheckConstraint, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from app.model.base import Base

class Subject (Base):
    __tablename__ = "subjects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False, index=True)
    subject_code = Column(String(50), unique=True, nullable=False, index=True)

    # Relationships
    exams = relationship("Exam", back_populates="subject", cascade="all, delete-orphan")


class Exam(Base):
    __tablename__ = "exams"

    id = Column(Integer, primary_key=True, index=True)
    subject_id = Column(Integer, ForeignKey("subjects.id"), nullable=False, index=True)
    exam_code = Column(String(50), unique=True, nullable=False, index=True)
    valid_date = Column(DateTime, nullable=False)
    start_time = Column(DateTime, nullable=False)
    duration = Column(Integer, nullable=False)  # Duration in minutes

    __table_args__ = (
        CheckConstraint(
            "duration > 0",
            name="check_exam_duration_positive"
        ),
        CheckConstraint(
            "valid_date < start_time",
            name="check_exam_valid_date_before_start_time"
        )
    )

    # Relationships
    subject = relationship("Subject", back_populates="exams")
    questions = relationship("ExamQuestion", back_populates="exam", cascade="all, delete-orphan")


class ExamQuestion(Base):
    __tablename__ = "exam_questions"

    id = Column(Integer, primary_key=True, index=True)
    exam_id = Column(Integer, ForeignKey("exams.id"), nullable=False, index=True)
    question_text = Column(String(500), nullable=False)

    # Relationships
    exam = relationship("Exam", back_populates="questions")
    options = relationship("QuestionOption", back_populates="question", cascade="all, delete-orphan")


class QuestionOption(Base):
    __tablename__ = "question_options"

    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, ForeignKey("exam_questions.id"), nullable=False, index=True)
    option_text = Column(String(200), nullable=False)
    is_correct = Column(Boolean, nullable=False, default="False")

    # Relationships
    question = relationship("ExamQuestion", back_populates="options")
