import json
from http.server import BaseHTTPRequestHandler
import urllib.parse
from weather import fetch_weather
import requests

class SlackRequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        # Parse request data
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        print("Received data:", post_data)

        # Parse URL-encoded data
        parsed_data = urllib.parse.parse_qs(post_data)
        print("Parsed data:", parsed_data)

        # Extract city parameter from Slack's slash command
        city = parsed_data.get('text', [''])[0]

        # Validate city parameter
        if not city:
            self.send_error(400, 'Missing city parameter')
            return    

        # check if correct JSON object is constructed.
        json_data = json.dumps({'text': city})
        print("Constructed JSON:", json_data)

        # Fetch weather data for the specified city
        temperature = fetch_weather(city)

        if temperature is None:
            # Handle error fetching weather data
            self.send_error(500, 'Error fetching weather data')
            return

        # Format response message with weather information
        response_message = f"The current temperature in {city} is {temperature:.0f}°C."

        try:
            # Send response to the provided response_url
            response_url = parsed_data.get('response_url', [''])[0]
            response_data = {'text': response_message}
            requests.post(response_url, json=response_data)

            # Send success response to Slack
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
        except Exception as e:
            # Handle any unexpected errors
            self.send_error(500, f'Error sending response: {str(e)}')