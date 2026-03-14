from datetime import datetime
from weather import get_weather
from nlp import nlp_processor
from dialog_manager import get_state, set_state, DialogState

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
    
def handle_weather(match):
    city = match.group(1)
    return get_weather(city)

def handle_weather_nlp(text):
    
    doc = nlp_processor.nlp(text)
    
    has_weather = False
    for token in doc:
        if token.lemma_ == "погода":
            has_weather = True
            break
    
    city = None
    city_lemma = None
    
    for ent in doc.ents:
        if ent.label_ in ["GPE", "LOC"]:
            city = ent.text

            first_token = ent[0]
            city_lemma = first_token.lemma_
            break
    
    if city and has_weather:

        weather_info = get_weather(city_lemma)
        return weather_info
    
    return "Не удалось определить город."

def handle_weather_dialog(user_id, text):
    state = get_state(user_id)
    
    if state == DialogState.START:

        doc = nlp_processor.process(text)
        city = None
        if doc:
            for ent in doc.ents:
                if ent.label_ in ["GPE", "LOC"]:
                    city = ent[0].lemma_
                    break
        
        if city:
            return get_weather(city)
        
        else:
            set_state(user_id, DialogState.WAIT_CITY)
            return "В каком городе?"
    
    elif state == DialogState.WAIT_CITY:
        city = text
        set_state(user_id, DialogState.START)
        return get_weather(city)