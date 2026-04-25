import whisper
import sounddevice as sd
import numpy as np
import re

model = whisper.load_model("small")

# Флаг для синхронизации
_is_tts_playing = False

def set_tts_playing(playing):
    global _is_tts_playing
    _is_tts_playing = playing

def is_tts_playing():
    return _is_tts_playing

def record_audio(seconds=4, fs=16000):
    """Запись звука с микрофона"""
    print("Говорите...")
    audio = sd.rec(int(seconds * fs), samplerate=fs, channels=1, dtype='float32')
    sd.wait()
    audio = audio.flatten()
    print("Запись завершена")
    return audio

def normalize_audio(audio):
    """Нормализация и усиление аудио (возвращает float32)"""
    # Усиление
    audio = audio * 50.0
    
    # Ограничиваем значения в пределах [-1, 1]
    audio = np.clip(audio, -1, 1)
    
    return audio.astype(np.float32)

def transcribe_audio(audio, sample_rate=16000):
    """Распознавание речи"""
    # Усиливаем аудио (оставляем float32)
    audio = normalize_audio(audio)
    
    try:
        result = model.transcribe(audio, language="ru", fp16=False)
        return result["text"]
    except Exception as e:
        print(f"[Whisper Error] {e}")
        return ""

def clean_text(text):
    """Очистка текста"""
    text = text.lower()
    text = re.sub(r"[^\w\sа-яё]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def listen():
    """Главная функция"""
    # Ждём, пока TTS закончит
    while is_tts_playing():
        import time
        time.sleep(0.1)

    audio = record_audio(seconds=4)
    raw_text = transcribe_audio(audio)
    print(f"Распознано: {raw_text}")
    
    if not raw_text:
        return ""
    
    cleaned = clean_text(raw_text)
    print(f"Очищено: {cleaned}")
    return cleaned

if __name__ == "__main__":
    text = listen()
    print(f"Результат: '{text}'")