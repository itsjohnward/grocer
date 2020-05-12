from datetime import datetime


def is_date(text):
    return isinstance(text, str) and (
        "Monday" in text
        or "Tuesday" in text
        or "Wednesday" in text
        or "Thursday" in text
        or "Friday" in text
        or "Saturday" in text
        or "Sunday" in text
    )


def is_time(text):
    return isinstance(text, str) and " - " in text and ("am" in text or "pm" in text)


def is_money(text):
    return isinstance(text, str) and "$" in text


def get_time_window(num_minutes=5):
    now = datetime.now()
    window = (now.minute // num_minutes) * num_minutes
    filename_str = "%Y%m%d-%H%M%S"
    return now.replace(minute=window, second=0, microsecond=0).strftime(filename_str)
