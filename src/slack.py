import json
from http.server import BaseHTTPRequestHandler
import urllib.parse
import hmac
import hashlib
from weather import fetch_weather
import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class SlackRequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        # Retrieve Slack signing secret from environment variable
        slack_signing_secret = os.environ.get('SLACK_SIGNING_SECRET')

        # Extract timestamp header from the request
        timestamp = self.headers['X-Slack-Request-Timestamp']

        # Extract raw request body
        content_length = int(self.headers['Content-Length'])
        request_body = self.rfile.read(content_length)

        # Concatenate version number, timestamp, and request body
        sig_basestring = f'v0:{timestamp}:{request_body.decode("utf-8")}'

        # Hash the basestring using the signing secret
        computed_signature = 'v0=' + hmac.new(slack_signing_secret.encode(), sig_basestring.encode(), hashlib.sha256).hexdigest()

        # Extract Slack signature from request headers
        slack_signature = self.headers['X-Slack-Signature']
        
        if not hmac.compare_digest(computed_signature, slack_signature):
            # Signatures do not match, reject the request
            self.send_error(401, 'Unauthorized: Signatures do not match')
            return

        # Process the request
        parsed_data = urllib.parse.parse_qs(request_body.decode("utf-8"))
        print("Parsed data:", parsed_data)

        # Extract city parameter from Slack's slash command
        city = parsed_data.get('text', [''])[0]

        # Validate city parameter
        if not city:
            # Missing city parameter, send error response
            self.send_error(400, 'Missing city parameter')
            return

        # Fetch weather data for the specified city
        temperature = fetch_weather(city)

        if temperature == 'city not found':
            # City not found, send response to Slack
            response_data = {'text': f"City '{city}' not found. Please confirm that you have entered the correct city."}
        elif temperature is None:
            # Error fetching weather data, send response to Slack
            response_data = {'text': 'Temperature for {city} not found.'}
        else:
            # Weather data fetched successfully, send response to Slack
            response_data = {'text': f"The current temperature in {city} is {temperature:.0f}°C."}

        try:
            # Send response to Slack using Ngrok URL
            ngrok_url = os.environ.get('NGROK_URL')
            if ngrok_url:
                response_url = parsed_data.get('response_url', [''])[0]
                requests.post(response_url, json=response_data)
                print("Response sent to Slack at:", response_url)  # Added to see where the response is being sent

                # Send success response to Slack
                self.send_response(200)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
            else:
                print("Ngrok URL not found. Make sure Ngrok is running and the NGROK_URL environment variable is set.")
        except Exception as e:
            # Handle any unexpected errors
            self.send_error(500, f'Error sending response: {str(e)}')
