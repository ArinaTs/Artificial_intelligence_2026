import pandas as pd
import joblib
import spacy
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

try:
    nlp = spacy.load("ru_core_news_md")
except:
    exit()

def get_text_vector(text):
    doc = nlp(text)
    return doc.vector

data = pd.read_csv("dataset.csv", encoding="utf-8")
texts = data["text"].tolist()
intents = data["intent"].tolist()

X = np.array([get_text_vector(text) for text in texts])

X_train, X_test, y_train, y_test = train_test_split(
    X, intents, test_size=0.2, random_state=42
)

model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

accuracy = model.score(X_test, y_test)

y_pred = model.predict(X_test)
print("\n   Classification Report:")
print(classification_report(y_test, y_pred))

joblib.dump(model, "model_embedding.pkl")

def predict_intent(text):
    vector = get_text_vector(text).reshape(1, -1)
    return model.predict(vector)[0]

print("\n8. Проверка на примерах:")
test_phrases = ["привет", "какое число", "сколько времени", "прощай", "что с погодой"]
for phrase in test_phrases:
    result = predict_intent(phrase)
    print(f"   '{phrase}' → {result}")
