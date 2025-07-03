import os
import re
import uuid
from typing import List
from docx import Document
import zipfile
from app.core.db_connect import SessionLocal
from app.model.models import Subject
from app.schema.schema import ExamPreview, QuestionPreview, QuestionChoice
from app.utils.date_time_utils import is_valid_date

IMAGE_FOLDER = "static/images"


def extract_exam_info(docx_path: str) -> ExamPreview:
    db = SessionLocal()
    doc = Document(docx_path)
    exam = ExamPreview()

    full_text = "\n".join(p.text.strip() for p in doc.paragraphs if p.text.strip())

    patterns = {
        "subject_code": r"Subject:\s*(.+)",
        "number_quiz": r"Number of Quiz:\s*(\d+)",
        "description": r"Lecturer:\s*(.+)",
        "start_date": r"Date:\s*([\d\w\-\/]+)",
    }
    subject_code = None

    for field, pattern in patterns.items():
        match = re.search(pattern, full_text, flags=re.IGNORECASE)
        if not match:
            continue

        value = match.group(1).strip()

        if field == "number_quiz":
            setattr(exam, field, int(value))
        elif field == "start_date":
            if value == "YYYY-MM-DD":
                exam.start_date = None
            elif is_valid_date(value, "%d-%m-%Y"):
                exam.start_date = value
            else:
                exam.start_date = None
        elif field == "subject_code":
            subject_code = value
        else:
            setattr(exam, field, value)


    # Query DB for subject_id if subject_code is found
    if subject_code:
        subject = db.query(Subject).filter(Subject.subject_code == subject_code).first()
        exam.subject_id = str(subject.id) if subject else None
    else:
        exam.subject_id = None

    return exam


def save_image_from_docx(docx_path: str) -> dict:
    image_map = {}
    with zipfile.ZipFile(docx_path) as docx_zip:
        for file in docx_zip.namelist():
            if file.startswith("word/media/"):
                ext = os.path.splitext(file)[1]
                img_data = docx_zip.read(file)
                filename = f"{uuid.uuid4()}{ext}"
                filepath = os.path.join(IMAGE_FOLDER, filename)
                with open(filepath, "wb") as f:
                    f.write(img_data)
                image_map[file.split("/")[-1]] = filepath
    return image_map


from typing import List
from docx import Document
import re
import os
import zipfile
from uuid import uuid4

from app.schema.schema import QuestionPreview, QuestionChoice


IMAGE_FOLDER = "static/images"


def save_image_from_docx(docx_path: str) -> dict:
    image_map = {}
    with zipfile.ZipFile(docx_path) as docx_zip:
        for file in docx_zip.namelist():
            if file.startswith("word/media/"):
                ext = os.path.splitext(file)[1]
                img_data = docx_zip.read(file)
                filename = f"{uuid4().hex}{ext}"
                filepath = os.path.join(IMAGE_FOLDER, filename)
                with open(filepath, "wb") as f:
                    f.write(img_data)
                image_map[file.split("/")[-1]] = filepath
    return image_map


def extract_questions(docx_path: str) -> List[QuestionPreview]:
    doc = Document(docx_path)
    questions: List[QuestionPreview] = []
    image_map = save_image_from_docx(docx_path)
    image_list = list(image_map.values())
    image_index = 0

    for table in doc.tables:
        q = QuestionPreview(options=[])
        correct_letter = None

        for row in table.rows:
            cells = [cell.text.strip() for cell in row.cells]
            print("ROW CELLS:", cells)  # Debugging line

            key, value = cells[0], cells[1]

            # Bỏ qua dòng QN
            if re.match(r"^QN=\d+", key, re.IGNORECASE):
                q.content = value.strip()
                continue

            # Đáp án đúng
            if re.match(r"^ANSWER\s*:?", key, re.IGNORECASE):
                correct_letter = value.strip().upper()
                continue

            # MARK
            if re.match(r"^MARK\s*:?", key, re.IGNORECASE):
                try:
                    q.mark = float(value.strip())
                except ValueError:
                    q.mark = 0.0
                continue

            # UNIT
            if re.match(r"^UNIT\s*:?", key, re.IGNORECASE):
                q.unit = value.strip()
                continue

            # MIX CHOICES
            if re.match(r"^MIX CHOICES\s*:?", key, re.IGNORECASE):
                q.mix_choices = value.strip().lower() == "yes"
                continue

            # Đáp án lựa chọn
            if re.match(r"^[a-dA-D]\.", key):
                q.options.append(
                    QuestionChoice(content=value.strip(), is_correct=False)
                )
                continue

            # Gán nội dung câu hỏi
            if not q.content:
                q.content = value
                continue

        # Gán hình nếu có
        if "file:" in (q.content or "").lower() and image_index < len(image_list):
            q.file_id = image_list[image_index]
            image_index += 1

        # Gán đáp án đúng
        if correct_letter:
            idx = ord(correct_letter) - ord("A")
            if 0 <= idx < len(q.options):
                q.options[idx].is_correct = True

        # Chỉ thêm nếu có nội dung hoặc ảnh và đáp án
        if (q.content or q.file_id) and q.options:
            questions.append(q)

    return questions



def parse_full_exam(docx_path: str) -> ExamPreview:
    exam = extract_exam_info(docx_path)
    exam.questions = extract_questions(docx_path)
    return exam
