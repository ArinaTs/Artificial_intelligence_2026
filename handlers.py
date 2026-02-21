from datetime import datetime

def handle_greeting(match=None):
    return "Здравствуйте! Чем могу помочь?"

def handle_farewell(match=None):
    return "До свидания!"

def handle_time(match=None):
    current_time = datetime.now().strftime("%H:%M")
    return f"Сейчас {current_time}."

def handle_date(match=None):
    current_date = datetime.now().strftime("%d.%m.%Y")
    return f"Сегодня {current_date}."

def handle_year(match=None):
    current_year = datetime.now().year
    return f"Сейчас {current_year} год."

def handle_how_are_you(match=None):
    return "У меня всё хорошо!"

def handle_unknown(match=None):
    return "Я не понимаю запрос."

def handle_calculation(match):
    expression = match.group(1)
    
    expression = expression.replace(" ", "")
    
    try:
        numbers = expression.split('+')
        
        if len(numbers) != 2:
            return "Нужно два числа через + (например: 5+3)"
        
        a = int(numbers[0])
        b = int(numbers[1])
        result = a + b
        
        return f"{a} + {b} = {result}"
    
    except (ValueError, IndexError):
        return "Ошибка! Нужно ввести числа через + (например: 5+3)"