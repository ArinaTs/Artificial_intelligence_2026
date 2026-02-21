import re
from patterns import get_patterns
from handlers import handle_farewell, handle_unknown
from logger import save_to_file

def process_message(message):
    message = message.strip().lower()
    patterns = get_patterns()
    
    for pattern, handler in patterns:
        match = pattern.search(message)
        if match:
            return handler(match)
    
    return handle_unknown()

def main():
    print("Бот запущен! Для выхода напишите 'пока/выход'")
    
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