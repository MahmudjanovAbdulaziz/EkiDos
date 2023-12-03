import requests
from datetime import datetime

def get_location():
    try:
        response = requests.get('https://ipinfo.io')
        return response.json().get('city', 'Unknown City')
    except Exception as e:
        print(f'Error getting location: {e}')
        return None

def get_current_time():
    try:
        response = requests.get('http://worldtimeapi.org/api/ip')
        return datetime.fromisoformat(response.json()['datetime']).strftime('%Y-%m-%d %H:%M:%S')
    except Exception as e:
        print(f"Error getting current time: {e}")
        return None

def get_weather(city):
    try:
        api_key = '674e9f7aff53df244de011df3f3c6e97'
        params = {'q': city, 'appid': api_key, 'units': 'metric'}
        response = requests.get('http://api.openweathermap.org/data/2.5/weather', params=params)
        data = response.json()
        return f"Weather in {city}: {data['weather'][0]['description']}, Temperature: {data['main']['temp']}°C"
    except Exception as e:
        print(f"Error getting weather: {e}")
        return None

if __name__ == "__main__":
    city = get_location()
    current_time = get_current_time()
    weather = get_weather(city)

    if city and current_time and weather:
        print(f"Город: {city}")
        print(f"Точное время: {current_time}")
        print(f"Погода: {weather}")
    else:
        print("Unable to retrieve information.")
