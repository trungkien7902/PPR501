from collections import defaultdict
from http import HTTPStatus
from typing import Any

from app.model.models import Subject, ExamQuestion, QuestionChoice, Account, Result, ResultDetail
from app.schema.schema import CustomException, ExamResponse, QuestionResponse, Options, TakeExamRequest, AuthRequest, \
    SubmitExamRequest, SubmitExamResponse
from app.model.models import Exam
from app.core.db_connect import SessionLocal
from app.service.auth_service import login
from datetime import datetime
from collections import defaultdict
from http import HTTPStatus

db = SessionLocal()


def get_exam_by_subject_code(subject_code: str) -> list[Any] | None:
    try:
        subject = db.query(Subject).filter(Subject.subject_code == subject_code).first()
        if not subject:
            raise CustomException(f"Môn học với mã {subject_code} không tồn tại.", HTTPStatus.NOT_FOUND)
        exams = db.query(Exam).filter(Exam.subject_id == subject.id).all()
        if not exams:
            return None
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


from contextlib import contextmanager

def get_exam_by_exam_code(exam_code: str, role_get_option: str = "Admin") -> ExamResponse:
    with SessionLocal() as db:
        exam = db.query(Exam).filter(Exam.name == exam_code).first()
        if not exam:
            raise CustomException(
                f"Bài kiểm tra với mã {exam_code} không tồn tại.", HTTPStatus.NOT_FOUND
            )

        subject = db.query(Subject).filter(Subject.id == exam.subject_id).first()
        if not subject:
            raise CustomException(
                f"Môn học với mã {exam.subject_id} không tồn tại.", HTTPStatus.NOT_FOUND
            )

        questions = db.query(ExamQuestion).filter(ExamQuestion.exam_id == exam.id).all()
        question_responses = []
        for q in questions:
            options = [
                Options(
                    id=choice.id,
                    question_id=q.id,
                    content=choice.content,
                    is_correct=choice.is_correct if role_get_option == "Admin" else None
                ) for choice in q.choices
            ]
            question_responses.append(
                QuestionResponse(
                    id=q.id,
                    content=q.content,
                    file_id=q.file_id,
                    mark=q.mark,
                    unit=q.unit,
                    mix_choices=q.mix_choices,
                    options=options
                )
            )

        return ExamResponse(
            id=exam.id,
            name=exam.name,
            subject_code=subject.subject_code,
            number_quiz=exam.number_quiz,
            valid_from=exam.valid_from.isoformat(),
            valid_to=exam.valid_to.isoformat(),
            duration_minutes=exam.duration_minutes,
            description=exam.description,
            questions=question_responses,
        )

def update_exam_by_exam_code(new_exam: ExamResponse) -> ExamResponse:
    try:
        exam = db.query(Exam).filter(Exam.name == new_exam.name).first()
        if not exam:
            raise CustomException(
                f"Bài kiểm tra với mã {new_exam.name} không tồn tại.",
                HTTPStatus.NOT_FOUND
            )

        # Cập nhật thông tin cơ bản
        exam.number_quiz = new_exam.number_quiz
        exam.valid_from = new_exam.valid_from
        exam.valid_to = new_exam.valid_to
        exam.duration_minutes = new_exam.duration_minutes
        exam.description = new_exam.description

        # Xóa toàn bộ câu hỏi cũ và choices cũ (do cascade)
        exam.questions.clear()

        # Thêm câu hỏi và option mới
        for question in new_exam.questions:
            new_question = ExamQuestion(
                content=question.content,
                file_id=question.file_id,
                mark=question.mark,
                unit=question.unit,
                mix_choices=question.mix_choices
            )

            for option in question.options:
                new_option = QuestionChoice(
                    content=option.content,
                    is_correct=option.is_correct
                )
                new_question.choices.append(new_option)

            exam.questions.append(new_question)

        db.commit()

        return ExamResponse(
            id=exam.id,
            name=exam.name,
            subject_code=new_exam.subject_code,
            number_quiz=exam.number_quiz,
            valid_from=exam.valid_from.isoformat(),
            valid_to=exam.valid_to.isoformat(),
            duration_minutes=exam.duration_minutes,
            description=exam.description,
            questions=new_exam.questions  # Trả lại đúng như input, hoặc có thể query lại nếu cần chính xác ID
        )

    except CustomException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        raise CustomException(f"Đã xảy ra lỗi hệ thống: {str(e)}", HTTPStatus.INTERNAL_SERVER_ERROR)
    finally:
        db.close()

def take_exam(take_exam_request: TakeExamRequest) -> ExamResponse:
    auth_request = AuthRequest(
        username=take_exam_request.username,
        password=take_exam_request.password
    )
    auth = login(auth_request)
    if not auth:
        raise CustomException("Thông tin đăng nhập không hợp lệ.", HTTPStatus.UNAUTHORIZED)

    account = db.query(Account).filter(Account.username == take_exam_request.username).first()
    if not account:
        raise CustomException(f"Tài khoản {take_exam_request.username} không tồn tại.", HTTPStatus.NOT_FOUND)
    if account.role != "STUDENT":
        raise CustomException("Chỉ sinh viên mới có thể tham gia bài kiểm tra.", HTTPStatus.FORBIDDEN)



    exam_response = get_exam_by_exam_code(take_exam_request.exam_code, role_get_option="Student")
    if not exam_response:
        raise CustomException(f"Bài kiểm tra với mã {take_exam_request.exam_code} không tồn tại.", HTTPStatus.NOT_FOUND)

    # Check thời gian hợp lệ của bài kiểm tra
    current_time = datetime.now()
    if current_time < datetime.fromisoformat(exam_response.valid_from) or current_time > datetime.fromisoformat(exam_response.valid_to):
        raise CustomException("Bài kiểm tra không còn hợp lệ trong thời gian này.", HTTPStatus.FORBIDDEN)
    # Trả về thông tin bài kiểm tra
    return exam_response


def submit(request: SubmitExamRequest):
    exam = db.query(Exam).filter(Exam.name == request.exam_code).first()
    if not exam:
        raise CustomException(f"Bài kiểm tra với mã {request.exam_code} không tồn tại.", HTTPStatus.NOT_FOUND)

    user = db.query(Account).filter(Account.username == request.username).first()
    if not user:
        raise CustomException(f"Người dùng với tên {request.username} không tồn tại.", HTTPStatus.NOT_FOUND)

    total_mark = 0
    correct = 0
    wrong = 0

    result = Result(
        exam_id=exam.id,
        student_id=user.id,
        score=0
    )
    db.add(result)
    db.flush()

    # Gom nhóm theo câu hỏi
    answer_dict = defaultdict(list)
    for answer in request.answers:
        answer_dict[answer.question_id].append(answer.option_id)

    detailed_result = []

    for question_id, selected_option_ids in answer_dict.items():
        question = db.query(ExamQuestion).filter(
            ExamQuestion.id == question_id,
            ExamQuestion.exam_id == exam.id
        ).first()

        if not question:
            raise CustomException(f"Câu hỏi với ID {question_id} không tồn tại trong bài kiểm tra.", HTTPStatus.NOT_FOUND)

        correct_choices = db.query(QuestionChoice).filter(
            QuestionChoice.question_id == question_id,
            QuestionChoice.is_correct == True
        ).all()

        correct_option_ids = {c.id for c in correct_choices}
        selected_option_ids_set = set(selected_option_ids)

        is_correct = False

        if question.mix_choices:
            # Câu hỏi checkbox: So sánh 2 tập hợp
            if selected_option_ids_set == correct_option_ids:
                is_correct = True
        else:
            # Câu hỏi radio: Chỉ được chọn 1
            if len(selected_option_ids) == 1 and selected_option_ids[0] in correct_option_ids:
                is_correct = True

        # Cộng điểm
        if is_correct:
            correct += 1
            total_mark += question.mark
        else:
            wrong += 1

        # Lưu chi tiết kết quả
        for opt_id in selected_option_ids:
            detail = ResultDetail(
                result_id=result.id,
                question_id=question_id,
                selected_option_id=opt_id
            )
            db.add(detail)

        detailed_result.append({
            "question_id": question_id,
            "selected_options": list(selected_option_ids),
            "correct_options": list(correct_option_ids),
            "is_correct": is_correct
        })

    # Cập nhật điểm tổng
    result.score = total_mark
    db.commit()

    return SubmitExamResponse(
        exam_code=request.exam_code,
        score=total_mark,
        total_questions=len(request.answers),
        correct_answers=correct,
        incorrect_answers=wrong
    )

