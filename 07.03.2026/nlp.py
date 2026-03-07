import spacy

class NLPProcessor:
    
    def __init__(self):

        self.nlp = None
        self.is_ready = False
    
    def initialize(self):

        try:
            self.nlp = spacy.load("ru_core_news_sm")
            self.is_ready = True
            print("NLP модель загружена")
            return True
        except:
            return False
    
    def process(self, text):

        if not self.is_ready:
            return None
        return self.nlp(text)
    
    def extract_cities(self, text):

        doc = self.nlp(text)
        for ent in doc.ents:
            if ent.label_ in ["GPE", "LOC"]:
                return ent.text
        return None
    
    def get_tokens_info(self, text):

        if not self.is_ready:
            return []
        
        doc = self.nlp(text)
        tokens_info = []
        
        for token in doc:
            tokens_info.append({
                'text': token.text,
                'lemma': token.lemma_,
                'pos': token.pos_,
                'is_stop': token.is_stop
            })
        
        return tokens_info
    
    def extract_date(self, text):
        if not self.is_ready:
            return None
    
        doc = self.nlp(text)
        for ent in doc.ents:
            if ent.label_ == "DATE":
                return ent.text
        return None

    def detect_intent(self, text):

        if not self.is_ready:
            return "unknown"
        
        doc = self.nlp(text)
        lemmas = [token.lemma_.lower() for token in doc]

        if "погода" in lemmas:
            return "weather"
        
        return "unknown"

nlp_processor = NLPProcessor()