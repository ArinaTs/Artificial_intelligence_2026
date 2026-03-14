import re
from patterns import get_patterns
from handlers import handle_farewell, handle_unknown, handle_weather_dialog
from logger import save_to_file
from database import init_db, get_or_create_user, is_new_user
from nlp import nlp_processor
from dialog_manager import get_state, DialogState

def detect_intent(text):
    """Определение намерения пользователя через NLP"""
    doc = nlp_processor.process(text)
    if doc:
        lemmas = [token.lemma_.lower() for token in doc]
        
        if "погода" in lemmas:
            return "weather"
    
    # Если NLP не сработал, проверяем по паттернам
    patterns = get_patterns()
    for pattern, handler in patterns:
        if pattern.search(text.lower()):
            if handler == handle_weather_dialog:
                return "weather"
            return handler.__name__
    
    return "unknown"

def process_message(user_id, message):
    message = message.strip().lower()

    intent = detect_intent(message)
    
    state = get_state(user_id)

    if state == DialogState.WAIT_CITY:
        return handle_weather_dialog(user_id, message)
    
    if intent == "weather":
        return handle_weather_dialog(user_id, message)

    patterns = get_patterns()
    for pattern, handler in patterns:
        match = pattern.search(message)
        if match:
            return handler(match)
    
    return handle_unknown()

def main():

    init_db()
    
    print("Загрузка NLP модели...")
    if nlp_processor.initialize():
        print("NLP модель готова к работе")
    else:
        print("NLP модель не загружена, бот будет работать в ограниченном режиме")
        
    print("Бот запущен! Для выхода напишите 'пока/выход'")
    print("Как вас зовут?")
    
    user_name = input("Вы: ").strip()
    user_id = get_or_create_user(user_name)
    

    if is_new_user(user_name):
        print(f"Бот: Приятно познакомиться, {user_name}!")
    else:
        print(f"Бот: С возвращением, {user_name}!")
    
    while True:
        user_input = input("Вы: ")
        
        if user_input.lower() in ["пока", "выход"]:
            print("Бот:", handle_farewell())
            break
        
        response = process_message(user_id, user_input)
        print("Бот:", response)
        
        save_to_file(user_input, response)

if __name__ == "__main__":
    main()