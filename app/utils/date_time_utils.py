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