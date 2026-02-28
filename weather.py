import requests

API_KEY = "my_api_key"

def get_weather(city):
    url = "http://api.weatherstack.com/current"
    params = {
        "access_key": API_KEY,
        "query": city
    }
    
    try:
        response = requests.get(url, params=params)
        data = response.json()
        
        if "error" in data:
            return "Ошибка: город не найден"
        
        temp = data["current"]["temperature"]
        wind = data["current"]["wind_speed"]
        desc = data["current"]["weather_descriptions"][0]
        
        return f"Погода в {city}: {temp}°C, ветер {wind} м/с, {desc}"
        
    except:
        return "Ошибка подключения"