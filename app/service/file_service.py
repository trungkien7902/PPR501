from docx import Document
import re

from app.model.exam_model import ExamQuestion, QuestionOption


def parse_questions_from_docx(file_path: str) -> list[ExamQuestion]:
    document = Document(file_path)
    lines = [p.text.strip() for p in document.paragraphs if p.text.strip()]
    result: list[ExamQuestion] = []
    idx = 0
    while idx < len(lines):
        # Handle question label: "Câu 1:", "câu1 :", "CAU    2   :"...
        if re.match(r'^c[âa]u\s*\d+\s*:', lines[idx], flags=re.IGNORECASE):
            question_text = re.sub(r'^c[âa]u\s*\d+\s*:\s*', '', lines[idx], flags=re.IGNORECASE)
            idx += 1

            # Handle option
            raw_options = []
            while idx < len(lines) and re.match(r'^[A-Ea-e]\.\s+', lines[idx]):
                label = lines[idx][0].upper()
                text = re.sub(r'^[A-Ea-e]\.\s*', '', lines[idx])
                raw_options.append((label, text))
                idx += 1

            # Handle answer
            correct_labels = []
            if idx < len(lines) and re.match(r'^đ[áaă]p\s*á[nn]\s*:', lines[idx], flags=re.IGNORECASE):
                match = re.search(r'^đ[áaă]p\s*á[nn]\s*:\s*([A-E](?:\s*,\s*[A-E])*)', lines[idx], flags=re.IGNORECASE)
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
