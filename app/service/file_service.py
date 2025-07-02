from docx import Document
import re

from app.model.exam_model import ExamQuestion, QuestionOption

# regex
QUESTION_LABEL_REGEX = r'^c[âa]u\s*\d+\s*:\s*' # Matches "câu 1:", "câu 2:", etc.
OPTION_LABEL_REGEX = r'^[A-Ea-e]\.\s+'         # Matches "A. ", "B. ", etc.
CORRECT_ANSWER_REGEX = r'^đ[áaă]p\s*á[nn]\s*:\s*([A-E](?:\s*,\s*[A-E])*)' # Matches "đáp án: A, B", "đáp án: C", etc.

def parse_questions_from_docx(file_path: str) -> list[ExamQuestion]:
    document = Document(file_path)
    lines = [p.text.strip() for p in document.paragraphs if p.text.strip()]
    result: list[ExamQuestion] = []
    idx = 0
    while idx < len(lines):
        # Handle question label:
        if re.match(QUESTION_LABEL_REGEX, lines[idx], flags=re.IGNORECASE):
            question_text = re.sub(QUESTION_LABEL_REGEX, '', lines[idx], flags=re.IGNORECASE)
            idx += 1

            # Handle option
            raw_options = []
            while idx < len(lines) and re.match(OPTION_LABEL_REGEX, lines[idx]):
                label = lines[idx][0].upper()
                text = re.sub(OPTION_LABEL_REGEX, '', lines[idx])
                raw_options.append((label, text))
                idx += 1

            # Handle answer
            correct_labels = []
            if idx < len(lines) and re.match(r'^đ[áaă]p\s*á[nn]\s*:', lines[idx], flags=re.IGNORECASE):
                match = re.search(CORRECT_ANSWER_REGEX, lines[idx], flags=re.IGNORECASE)
                if match:
                    correct_labels = [s.strip().upper() for s in match.group(1).split(",")]
                idx += 1

            # Create ExamQuestion object
            question = ExamQuestion(question_text=question_text)
            question.options = [
                QuestionOption(option_text=opt_text, is_correct=(label in correct_labels))
                for label, opt_text in raw_options
            ]

            result.append(question)

        else:
            idx += 1
    return result
