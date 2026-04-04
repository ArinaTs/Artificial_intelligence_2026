import torch
from datetime import datetime
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from nlp_utils import extract_city
from dialog_manager import get_state, set_state, DialogState
from weather import get_weather
from database import init_db, get_or_create_user, is_new_user, save_message

MODEL_NAME = "intent_model"

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)
model.eval()

label_map = {
    0: "greeting",
    1: "goodbye",
    2: "time",
    3: "date",
    4: "year",
    5: "how_are_you",
    6: "weather",
}

def predict_intent(text: str) -> str:
    inputs = tokenizer(text, return_tensors="pt", truncation=True)
    
    with torch.no_grad():
        outputs = model(**inputs)
    
    logits = outputs.logits
    predicted_class = torch.argmax(logits, dim=1).item()
    
    return label_map[predicted_class]

def handle_message(user_id: int, text: str) -> str:
    state = get_state(user_id)
    intent = predict_intent(text)

    if state == DialogState.WAIT_CITY:
        city = text
        weather = get_weather(city)
        set_state(user_id, DialogState.START)
        return weather

    if intent == "weather":
        city = extract_city(text)
        if city:
            return get_weather(city)
        else:
            set_state(user_id, DialogState.WAIT_CITY)
            return "В каком городе вас интересует погода?"

    elif intent == "greeting":
        return "Здравствуйте!"

    elif intent == "time":
        return f"Сейчас {datetime.now().strftime('%H:%M')}."

    elif intent == "date":
        return f"Сегодня {datetime.now().strftime('%d.%m.%Y')}."

    elif intent == "year":
        return f"Сейчас {datetime.now().year} год."

    elif intent == "goodbye":
        return "До свидания!"

    elif intent == "how_are_you":
        return "У меня всё хорошо!"

    return "Я не понял запрос."

def main():
    init_db()
    
    print("Бот запущен! Для выхода напишите 'пока/выход'")
    print("Как вас зовут?")
    
    user_name = input("Вы: ").strip()
    user_id = get_or_create_user(user_name)
    
    if is_new_user(user_name):
        print(f"Бот: Приятно познакомиться, {user_name}!")
    else:
        print(f"Бот: С возвращением, {user_name}!")
    
    while True:
        user_input = input("\nВы: ")
        
        if user_input.lower() in ["пока", "выход"]:
            print("Бот: До свидания!")
            break
        
        response = handle_message(user_id, user_input)
        print("Бот:", response)
        
        save_message(user_input, response)

if __name__ == "__main__":
    main()