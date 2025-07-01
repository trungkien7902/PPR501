def insert_question_to_exam(db, exam_id, question_data):
    from app.model.exam_model import ExamQuestion, QuestionOption

    # Create the question instance
    question = ExamQuestion(
        exam_id=exam_id,
        question_text=question_data['question_text']
    )

    # Add the question to the session
    db.add(question)
    db.flush()  # Flush to get the question ID for options

    # Create options for the question
    for option_text, is_correct in question_data['options'].items():
        option = QuestionOption(
            question_id=question.id,
            option_text=option_text,
            is_correct=is_correct
        )
        db.add(option)

    db.commit()
    return question.id  # Return the ID of the newly created question