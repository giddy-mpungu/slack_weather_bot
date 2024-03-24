import requests
import os
from dotenv import load_dotenv
import traceback

# Load environment variables from .env file
load_dotenv()

def fetch_weather(city):
    api_key = os.environ.get('OPENWEATHERMAP_API_KEY')  # OpenWeather API key
    
    # Construct the API request URL with only the city name
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&APPID={api_key}'
    
    try:
        # Send the API request
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        
        # Parse the JSON response
        data = response.json()
        
        # Extract temperature from the response
        if 'main' in data and 'temp' in data['main']:
            temperature_celsius = data['main']['temp']
            return temperature_celsius
        else:
            print(f'Error: Temperature data not found in response for {city}')
            return None
        
    except requests.exceptions.RequestException as e:
        print(f'Error fetching weather data: {e}')
        traceback.print_exc()
        return None
