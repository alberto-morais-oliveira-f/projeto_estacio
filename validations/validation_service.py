import re


def is_valid_email(email):
    """Validate email using a regular expression."""
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(pattern, email) is not None


def is_valid_phone(phone):
    """Validate phone number to match (xx) xxxxx-xxxx pattern."""
    pattern = r'^\(\d{2}\) \d{4,5}-\d{4}$'
    return re.match(pattern, phone) is not None
