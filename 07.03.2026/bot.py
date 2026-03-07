import re
from patterns import get_patterns
from handlers import handle_farewell, handle_unknown, handle_weather_nlp
from logger import save_to_file
from database import init_db, save_user
from nlp import nlp_processor

def process_message(message):
    message = message.strip().lower()
    patterns = get_patterns()
        
    if nlp_processor.is_ready:

        doc = nlp_processor.process(message)
        if doc:
            lemmas = [token.lemma_ for token in doc]
            
            if "погода" in lemmas:
                return handle_weather_nlp(message)
            
    message_lower = message.lower()
    for pattern, handler in patterns:
        match = pattern.search(message_lower)
        if match:

            if handler == handle_weather_nlp:
                continue
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
    save_user(user_name)
    print(f"Бот: Приятно познакомиться, {user_name}!")
    
    while True:
        user_input = input("Вы: ")
        
        if user_input.lower() in ["пока", "выход"]:
            print("Бот:", handle_farewell())
            break
        
        response = process_message(user_input)
        print("Бот:", response)
        
        save_to_file(user_input, response)

if __name__ == "__main__":
    main()