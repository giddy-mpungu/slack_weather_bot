import requests

def fetch_weather(city):
    api_key = 'efe2b207d4129a19e9107cc30fe4db47'  # Replace with your OpenWeather API key
    
    # Step 1: Get latitude and longitude coordinates using direct geocoding
    geo_url = f'http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={api_key}'
    try:
        geo_response = requests.get(geo_url)
        geo_response.raise_for_status()  # Raise an exception for HTTP errors
        geo_data = geo_response.json()
        
        # Extract latitude and longitude coordinates from the response
        if geo_data:
            lat = geo_data[0]['lat']
            lon = geo_data[0]['lon']
        else:
            print(f'Error: Could not find coordinates for {city}')
            return None
    except requests.exceptions.RequestException as e:
        print(f'Error fetching coordinates: {e}')
        return None
    
    # Step 2: Fetch weather data using latitude and longitude coordinates
    weather_url = f'http://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exclude=minutely,daily,alerts&appid={api_key}&units=metric'
    try:
        response = requests.get(weather_url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()
        temperature = data['current']['temp']
        return temperature
    except requests.exceptions.RequestException as e:
        print(f'Error fetching weather data: {e}')
        return None
