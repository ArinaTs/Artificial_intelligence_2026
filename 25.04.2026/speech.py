import threading
import pythoncom
import win32com.client
import re
from num2words import num2words
from voice import set_tts_playing

def normalize_text(text):

    def num_to_words(match):
        try:
            return num2words(int(match.group()), lang='ru')
        except:
            return match.group()
    text = re.sub(r'\d+', num_to_words, text)
    
    text = text.replace('°C', ' градусов цельсия')
    text = text.replace('м/с', ' метров в секунду')
    text = text.replace('км/ч', ' километров в час')
    
    return text

def speak_async(text):

    def _speak():
        pythoncom.CoInitialize()
        try:
            set_tts_playing(True)  # Начало речи
            normalized = normalize_text(text)
            speaker = win32com.client.Dispatch("SAPI.SpVoice")
            speaker.Speak(normalized)
        except Exception as e:
            print(f"[TTS Error] {e}")
        finally:
            set_tts_playing(False)  # Конец речи
            pythoncom.CoUninitialize()
    
    threading.Thread(target=_speak, daemon=True).start()