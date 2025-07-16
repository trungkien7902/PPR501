from http import HTTPStatus

from app.core.db_connect import SessionLocal
from app.model.models import ExamQuestion, QuestionChoice, Result, Exam
from app.schema.schema import QuestionResponse, CustomException, QuestionChoiceResponse, TakeExamRequest, AuthRequest
from typing import List

from app.service.auth_service import login

db = SessionLocal()


def get_question_choices_by_question_id(question_id: int) -> List[QuestionChoiceResponse]:
    try:
        question_choices = db.query(QuestionChoice).filter(QuestionChoice.question_id == question_id)
        if not question_choices:
            raise CustomException(f"Câu hỏi với id là {question_id} bị lỗi không có đáp án.", HTTPStatus.NOT_FOUND)
        question_choices_responses = []
        for question_choice in question_choices:
            question_choices_responses.append(QuestionChoiceResponse(
                id=question_choice.id,
                question_id=question_choice.question_id,
                content=question_choice.content,
            ))
        return question_choices_responses
    except CustomException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        raise CustomException(f"Đã xảy ra lỗi hệ thống: {str(e)}", HTTPStatus.INTERNAL_SERVER_ERROR)
    finally:
        db.close()


def get_questions_by_exam_id(exam_id: int) -> List[QuestionResponse]:
    try:
        questions = db.query(ExamQuestion).filter(ExamQuestion.exam_id == exam_id).first()
        if not questions:
            raise CustomException(f"Không có câu hỏi nào thuộc bài thi với id là {exam_id}.", HTTPStatus.NOT_FOUND)
        questions_responses = []
        for question in questions:
            questions_responses.append(QuestionResponse(
                id=question.id,
                exam_id=exam_id,
                content=question.content,
                file_id=question.file_id,
                mark=question.mark,
                unit=question.unit,
                mix_choices=question.mix_choices,
                questionChoices=get_question_choices_by_question_id(question.id, False)
            ))
        return questions_responses
    except CustomException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        raise CustomException(f"Đã xảy ra lỗi hệ thống: {str(e)}", HTTPStatus.INTERNAL_SERVER_ERROR)
    finally:
        db.close()


def submit_exam(answers: List[QuestionResponse], exam_id: int, student_id: int) -> str:
    try:
        if not answers:
            raise CustomException(f"Hệ thống không nhận được câu trả lời nào, vui lòng kiểm tra lại.", HTTPStatus.NOT_FOUND)
        correct_answers_mark=0
        total_mark=0
        for answer in answers:
            question_choice_correct = db.query(QuestionChoice).filter(QuestionChoice.question_id == answer.id and QuestionChoice.is_correct == True).first()
            if not question_choice_correct:
                raise CustomException(f"Không tìm thấy đáp án của câu hỏi với id là {answer.id}.", HTTPStatus.NOT_FOUND)
            total_mark += question_choice_correct.mark
            if question_choice_correct.id == answer.selectedChoice:
                correct_answers_mark += question_choice_correct.mark
        db.query(Result).add(Result(
            exam_id=exam_id,
            student_id=student_id,
            score=correct_answers_mark
        ))
        db.commit()
        return f"Tổng số điểm của bạn là {correct_answers_mark}/{total_mark}"
    except CustomException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        raise CustomException(f"Đã xảy ra lỗi hệ thống: {str(e)}", HTTPStatus.INTERNAL_SERVER_ERROR)
    finally:
        db.close()


