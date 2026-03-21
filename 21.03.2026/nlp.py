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
    

nlp_processor = NLPProcessor()