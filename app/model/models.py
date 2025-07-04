from sqlalchemy import (
    Column, Integer, String, Boolean, Text, Float, DateTime,
    ForeignKey, CheckConstraint
)
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


# ----------------- Account -----------------
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

    results = relationship("Result", back_populates="student", cascade="all, delete-orphan")
    assignments = relationship("SubjectAssign", back_populates="account", cascade="all, delete-orphan")
    exam_assignments = relationship("ExamAssign", back_populates="account", cascade="all, delete-orphan")


# ----------------- Subject -----------------
class Subject(Base):
    __tablename__ = "subjects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False, index=True)
    subject_code = Column(String(50), unique=True, nullable=False, index=True)

    exams = relationship("Exam", back_populates="subject", cascade="all, delete-orphan")
    assignments = relationship("SubjectAssign", back_populates="subject")


# ----------------- SubjectAssign -----------------
class SubjectAssign(Base):
    __tablename__ = "subject_assigns"

    id = Column(Integer, primary_key=True, index=True)
    subject_id = Column(Integer, ForeignKey("subjects.id"), nullable=False, index=True)
    account_id = Column(Integer, ForeignKey("accounts.id"), nullable=False, index=True)

    subject = relationship("Subject", back_populates="assignments")
    account = relationship("Account", back_populates="assignments")


# ----------------- Exam -----------------
class Exam(Base):
    __tablename__ = "exams"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, index=True)
    subject_id = Column(Integer, ForeignKey("subjects.id"), nullable=False, index=True)
    number_quiz = Column(Integer, nullable=False)
    valid_from = Column(DateTime, nullable=False)
    valid_to = Column(DateTime, nullable=False)
    duration_minutes = Column(Integer, nullable=False)
    description = Column(Text, nullable=True)
    is_active = Column(String(20), default=True)

    subject = relationship("Subject", back_populates="exams")
    questions = relationship("ExamQuestion", back_populates="exam", cascade="all, delete-orphan")
    results = relationship("Result", back_populates="exam", cascade="all, delete-orphan")
    assignments = relationship("ExamAssign", back_populates="exam", cascade="all, delete-orphan")


# ----------------- ExamQuestion -----------------
class ExamQuestion(Base):
    __tablename__ = "exam_questions"

    id = Column(Integer, primary_key=True, index=True)
    exam_id = Column(Integer, ForeignKey("exams.id"), nullable=False, index=True)
    content = Column(Text, nullable=False)
    file_id = Column(String, nullable=True)
    mark = Column(Float, nullable=False, default=1.0)
    unit = Column(String, nullable=True)
    mix_choices = Column(Boolean, default=False)

    exam = relationship("Exam", back_populates="questions")
    choices = relationship("QuestionChoice", back_populates="question", cascade="all, delete-orphan")
    details = relationship("ResultDetail", back_populates="question", cascade="all, delete-orphan")


# ----------------- QuestionChoice -----------------
class QuestionChoice(Base):
    __tablename__ = "question_choices"

    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, ForeignKey("exam_questions.id"), nullable=False, index=True)
    content = Column(Text, nullable=False)
    is_correct = Column(Boolean, default=False)

    question = relationship("ExamQuestion", back_populates="choices")
    result_details = relationship("ResultDetail", back_populates="selected_option", cascade="all, delete-orphan")


# ----------------- ExamAssign -----------------
class ExamAssign(Base):
    __tablename__ = "exam_assigns"

    id = Column(Integer, primary_key=True, index=True)
    exam_id = Column(Integer, ForeignKey("exams.id"), nullable=False, index=True)
    account_id = Column(Integer, ForeignKey("accounts.id"), nullable=False, index=True)

    exam = relationship("Exam", back_populates="assignments")
    account = relationship("Account", back_populates="exam_assignments")


# ----------------- Result -----------------
class Result(Base):
    __tablename__ = "results"

    id = Column(Integer, primary_key=True, index=True)
    exam_id = Column(Integer, ForeignKey("exams.id"), nullable=False, index=True)
    student_id = Column(Integer, ForeignKey("accounts.id"), nullable=False, index=True)
    score = Column(Integer, nullable=False)

    __table_args__ = (
        CheckConstraint("score >= 0", name="check_result_score_non_negative"),
    )

    exam = relationship("Exam", back_populates="results")
    student = relationship("Account", back_populates="results")
    details = relationship("ResultDetail", back_populates="result", cascade="all, delete-orphan")


# ----------------- ResultDetail -----------------
class ResultDetail(Base):
    __tablename__ = "result_details"

    id = Column(Integer, primary_key=True, index=True)
    result_id = Column(Integer, ForeignKey("results.id"), nullable=False, index=True)
    question_id = Column(Integer, ForeignKey("exam_questions.id"), nullable=False, index=True)
    selected_option_id = Column(Integer, ForeignKey("question_choices.id"), nullable=True)

    result = relationship("Result", back_populates="details")
    question = relationship("ExamQuestion", back_populates="details")
    selected_option = relationship("QuestionChoice", back_populates="result_details")
