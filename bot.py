import re
from patterns import get_patterns
from handlers import handle_farewell, handle_unknown
from logger import save_to_file
from database import init_db, save_user

def process_message(message):
    message = message.strip().lower()
    patterns = get_patterns()
    
    for pattern, handler in patterns:
        match = pattern.search(message)
        if match:
            return handler(match)
    
    return handle_unknown()

def main():

    init_db()
    
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