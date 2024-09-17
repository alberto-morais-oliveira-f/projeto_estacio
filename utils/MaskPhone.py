import re


def format_phone_number(digits):
    formatted_value = ""
    length = len(digits)
    if length > 0:
        formatted_value += f"({digits[:2]}"
    if length > 2:
        formatted_value += f") {digits[2:7]}"
    if length > 7:
        formatted_value += f"-{digits[7:11]}"
    return formatted_value[:15]


def format_phone(phone):
    digits = re.sub(r'\D', '', phone)
    formatted_value = format_phone_number(digits)
    return formatted_value


class MaskPhone:
    def __init__(self, phone_var, phone_entry):
        self.phone_var = phone_var
        self.phone_entry = phone_entry
        self.phone_trace_id = self.phone_var.trace_add('write', self.format_phone_entry)
        self.format_phone_entry()

    def format_phone_entry(self, *_):
        value = self.phone_var.get()
        digits = re.sub(r'\D', '', value)
        formatted_value = format_phone_number(digits)
        self.phone_var.trace_remove('write', self.phone_trace_id)
        self.phone_var.set(formatted_value)
        self.phone_trace_id = self.phone_var.trace_add('write', self.format_phone_entry)
        self.phone_entry.after(1, lambda: self.phone_entry.icursor(len(self.phone_var.get())))
