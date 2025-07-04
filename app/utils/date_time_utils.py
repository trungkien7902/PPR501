from datetime import datetime

def is_valid_date(date_str: str, format: str = "%Y-%m-%d") -> bool:
    """
    Kiểm tra xem date_str có hợp lệ theo định dạng format không.
    """
    try:
        datetime.strptime(date_str, format)
        return True
    except ValueError:
        return False

def convert_to_datetime(date_str: str | None, format: str = "%Y-%m-%d") -> datetime | None:
    """
    Chuyển đổi chuỗi date_str sang datetime. Nếu không hợp lệ, trả về None.
    """
    try:
        return datetime.strptime(date_str, format) if date_str else None
    except ValueError:
        return None
