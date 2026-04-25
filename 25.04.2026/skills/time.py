from datetime import datetime

def time_skill() -> str:
    return f"Сейчас {datetime.now().strftime('%H:%M')}."