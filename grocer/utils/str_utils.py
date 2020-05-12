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
