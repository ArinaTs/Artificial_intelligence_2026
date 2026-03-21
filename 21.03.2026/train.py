import pandas as pd
import spacy
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report

nlp = spacy.load("ru_core_news_sm")

def preprocess(text):
    doc = nlp(text)
    tokens = []
    for token in doc:
        if not token.is_punct and not token.is_space:
            if token.is_stop and token.lemma_ not in ["какой", "какая", "какое", "сколько", "который", "что"]:
                continue
            tokens.append(token.lemma_)
    return " ".join(tokens)

data = pd.read_csv("dataset.csv", encoding="utf-8-sig")
texts = data["text"].tolist()
intents = data["intent"].tolist()
processed_texts = [preprocess(text) for text in texts]

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(processed_texts)

X_train, X_test, y_train, y_test = train_test_split(
    X, intents, test_size=0.2, random_state=42
)

model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

accuracy = model.score(X_test, y_test)
print("Accuracy:", accuracy)

y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))

joblib.dump(model, "model.pkl")
joblib.dump(vectorizer, "vectorizer.pkl")

def predict_intent(text):
    processed = preprocess(text)
    vector = vectorizer.transform([processed])
    return model.predict(vector)[0]

test_text = "какая дата"
print(f"'{test_text}' → {predict_intent(test_text)}")