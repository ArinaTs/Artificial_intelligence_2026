import joblib
import spacy
from datetime import datetime
from logger import save_to_file
from database import init_db, get_or_create_user, is_new_user
from dialog_manager import get_state, set_state, DialogState
from weather import get_weather

nlp = spacy.load("ru_core_news_sm")
model = joblib.load("model.pkl")
vectorizer = joblib.load("vectorizer.pkl")

# Функция предобработки
def preprocess(text):
    doc = nlp(text)
    tokens = []
    for token in doc:
        if not token.is_punct and not token.is_space:
            if token.is_stop and token.lemma_ not in ["какой", "какая", "какое", "сколько", "который", "что"]:
                continue
            tokens.append(token.lemma_)
    return " ".join(tokens)

def predict_with_confidence(text):
    processed = preprocess(text)
    vector = vectorizer.transform([processed])
    probabilities = model.predict_proba(vector)
    confidence = max(probabilities[0])
    intent = model.predict(vector)[0]
    return intent, confidence

def extract_city(text):
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ in ["GPE", "LOC"]:
            return ent.text
    return None

def process_message(user_id, message):
    state = get_state(user_id)
    
    if state == DialogState.WAIT_CITY:
        city = message
        set_state(user_id, DialogState.START)
        return get_weather(city)
    
    intent, confidence = predict_with_confidence(message)
    
    if confidence < 0.25:
        return "Не уверен в ответе"
    
    if intent == "weather":
        city = extract_city(message)
        if city:
            return get_weather(city)
        else:
            set_state(user_id, DialogState.WAIT_CITY)
            return "Укажите город"
    
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
    
    else:
        return "Я не понял запрос"

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
        
        response = process_message(user_id, user_input)
        print("Бот:", response)
        
        save_to_file(user_input, response)

if __name__ == "__main__":
    main()