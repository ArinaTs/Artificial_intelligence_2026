import re
from handlers import (
    handle_greeting, handle_farewell, handle_time,
    handle_date, handle_year, handle_how_are_you,
    handle_calculation
)

# Словарь с паттернами и соответствующими обработчиками
patterns = [
    (re.compile(r"(привет|здравствуй|здравствуйте|добрый день)", re.IGNORECASE), handle_greeting),
    (re.compile(r"(пока|до свидания|всего доброго)", re.IGNORECASE), handle_farewell),
    (re.compile(r"(сколько времени|который час)", re.IGNORECASE), handle_time),
    (re.compile(r"(какая дата|какое сегодня число)", re.IGNORECASE), handle_date),
    (re.compile(r"(какой год|который год)", re.IGNORECASE), handle_year),
    (re.compile(r"(как дела|как ты)", re.IGNORECASE), handle_how_are_you),
    (re.compile(r"(\d+\s*\+\s*\d+)"), handle_calculation),
]

def get_patterns():
    return patterns