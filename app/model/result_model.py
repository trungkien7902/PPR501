from sqlalchemy import Column, Integer, String, CheckConstraint, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from app.model.base import Base

class Result(Base):
    __tablename__ = "results"

    id = Column(Integer, primary_key=True, index=True)
    exam_id = Column(Integer, ForeignKey("exams.id"), nullable=False, index=True)
    student_id = Column(Integer, ForeignKey("accounts.id"), nullable=False, index=True)
    score = Column(Integer, nullable=False)

    __table_args__ = (
        CheckConstraint(
            "score >= 0",
            name="check_result_score_non_negative"
        ),
    )

    # Relationships
    exam = relationship("Exam", back_populates="results")
    student = relationship("Student", back_populates="results")

class ResultDetail(Base):
    __tablename__ = "result_details"

    id = Column(Integer, primary_key=True, index=True)
    result_id = Column(Integer, ForeignKey("results.id"), nullable=False, index=True)
    question_id = Column(Integer, ForeignKey("exam_questions.id"), nullable=False, index=True)
    selected_option_id = Column(Integer, ForeignKey("question_options.id"), nullable=True)

    # Relationships
    result = relationship("Result", back_populates="details")
    question = relationship("ExamQuestion", back_populates="details")
    selected_option = relationship("QuestionOption", back_populates="result_details")