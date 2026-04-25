import spacy

nlp = spacy.load("ru_core_news_md")

def extract_city(text: str):
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ == "LOC":
            return ent.text
    return None