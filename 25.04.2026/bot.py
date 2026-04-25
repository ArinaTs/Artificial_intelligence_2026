import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from dialog_manager import get_state, set_state, DialogState
from speech import speak_async
from database import init_db, get_or_create_user, is_new_user, save_message
from skills import (
    weather_skill, time_skill, date_skill,
    greeting_skill, goodbye_skill, help_skill, smalltalk_skill, year_skill
)
from voice import listen

MODEL_PATH = "intent_model"

tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)
model.eval()

label_map = {
    0: "greeting",
    1: "goodbye",
    2: "time",
    3: "date",
    4: "year",
    5: "weather",
    6: "smalltalk",
    7: "help",
    8: "unknown"
}

def predict_intent(text: str) -> str:
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=128)
    
    with torch.no_grad():
        outputs = model(**inputs)
        
    logits = outputs.logits
    probabilities = torch.softmax(logits, dim=1)
    confidence = torch.max(probabilities).item()
    predicted_class = torch.argmax(logits, dim=1).item()
    
    return label_map[predicted_class], confidence

def route_intent(intent: str, text: str, user_id: int) -> str:
    
    if intent == "weather":
        return weather_skill(text, user_id)
    elif intent == "time":
        return time_skill()
    elif intent == "date":
        return date_skill()
    elif intent == "year":
        return year_skill()
    elif intent == "greeting":
        return greeting_skill()
    elif intent == "goodbye":
        return goodbye_skill()
    elif intent == "help":
        return help_skill()
    elif intent == "smalltalk":
        return smalltalk_skill(text)
    elif intent == "unknown":
        return "Я не понял запрос. Попробуйте переформулировать."

def handle_message(user_id: int, text: str) -> str:
    state = get_state(user_id)
    
    if state == DialogState.WAIT_CITY:
        response = weather_skill(text, user_id)
        speak_async(response)
        return response
    
    intent, confidence = predict_intent(text)
    print(f"[DEBUG] text: '{text}' → intent: {intent}, confidence: {confidence:.4f}")
    
    response = route_intent(intent, text, user_id)
    speak_async(response)
    return response

def main():
    init_db()
    
    print("Бот запущен! Для выхода скажите 'пока/выход/стоп/до свидания'")
    print("Пожалуйста, напишите как вас зовут?")
    
    user_name = input("Вы: ").strip()
    user_id = get_or_create_user(user_name)
    
    if is_new_user(user_name):
        welcome_text = f"Приятно познакомиться, {user_name}!"
        print(f"Бот: {welcome_text}")
        speak_async(welcome_text)
    else:
        welcome_text = f"С возвращением, {user_name}!"
        print(f"Бот: {welcome_text}")
        speak_async(welcome_text)
    
    while True:
        print("\n")
        user_input = listen()
        
        if user_input.lower() in ["пока", "выход", "стоп", "до свидания"]:
            print("Бот:", goodbye_skill())
            speak_async(goodbye_skill())
            break
        
        response = handle_message(user_id, user_input)
        print("Бот:", response)
        
        save_message(user_input, response)
        

if __name__ == "__main__":
    main()