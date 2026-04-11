from weather import get_weather
from nlp_utils import extract_city
from dialog_manager import get_state, set_state, DialogState

def weather_skill(text: str, user_id: int) -> str:
    state = get_state(user_id)
    
    if state == DialogState.WAIT_CITY:
        city = text
        set_state(user_id, DialogState.START)
        return get_weather(city)
    
    city = extract_city(text)
    if city:
        return get_weather(city)
    else:
        set_state(user_id, DialogState.WAIT_CITY)
        return "В каком городе вас интересует погода?"