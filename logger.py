from datetime import datetime

def save_to_file(user_message, bot_response):
    with open("chat_log.txt", "a", encoding="utf-8") as file:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        file.write(f"[{current_time}]\n")
        file.write(f"Вы: {user_message}\n")
        file.write(f"Бот: {bot_response}\n")
        file.write("-" * 40 + "\n")