from datetime import datetime


def get_greeting(current_time: str) -> str:
    """Принимает строку вида '2021-12-21 18:30:15' и возвращает приветствие."""
    time_obj = datetime.strptime(current_time, "%Y-%m-%d %H:%M:%S")

    hour = time_obj.hour

    if 6 <= hour < 12:
        greeting = "Доброе утро"
    elif 12 <= hour < 18:
        greeting = "Добрый день"
    elif 18 <= hour < 23:
        greeting = "Добрый вечер"
    else:
        greeting = "Доброй ночи"

    return greeting
