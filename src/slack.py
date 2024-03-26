import os
import hmac
import hashlib
import urllib.parse
import requests
from http.server import BaseHTTPRequestHandler
from dotenv import load_dotenv
from weather import fetch_weather

# Load environment variables from .env file
load_dotenv()

class SlackRequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        # Extract and decode request body
        request_body = self.extract_request_body()

        # Validate signature
        if not self.validate_signature(request_body):
            self.send_error(401, 'Unauthorized: Signatures do not match')
            return

        # Get parsed data
        parsed_data = self.process_request(request_body)

        # Get city 
        city = self.get_city(parsed_data)

        # Get temperature and handle errors
        temperature = None
        if city:
            temperature = self.get_temperature(city)

        # Send response to Slack
        self.send_slack_response(parsed_data, city, temperature)

    def extract_request_body(self):
        content_length = int(self.headers['Content-Length'])
        request_body = self.rfile.read(content_length).decode('utf-8')
        return request_body

    def validate_signature(self, request_body):
        slack_signing_secret = os.environ.get('SLACK_SIGNING_SECRET')
        timestamp = self.headers['X-Slack-Request-Timestamp']
        sig_basestring = f'v0:{timestamp}:{request_body}'
        computed_signature = 'v0=' + hmac.new(slack_signing_secret.encode(), sig_basestring.encode(), hashlib.sha256).hexdigest()
        slack_signature = self.headers['X-Slack-Signature']
        return hmac.compare_digest(computed_signature, slack_signature)

    def process_request(self, request_body):
        return urllib.parse.parse_qs(request_body)

    def get_city(self, parsed_data):
        return parsed_data.get('text', [''])[0]

    def get_temperature(self, city):
        return fetch_weather(city)

    def send_slack_response(self, parsed_data, city, temperature):
        try:
            if not city:
                response_data = {'text': 'Please enter a city'}
            elif temperature == 'city not found':
                response_data = {'text': f"City '{city}' not found. Please confirm that you have entered the correct city."}
            elif temperature is None:
                response_data = {'text': f"Temperature for {city} not found."}
            else:
                response_data = {'text': f"The current temperature in {city} is {temperature:.0f}°C."}

            ngrok_url = os.environ.get('NGROK_URL')
            if ngrok_url:
                response_url = parsed_data.get('response_url', [''])[0]
                requests.post(response_url, json=response_data)
                print("Response sent to Slack at:", response_url)  
                self.send_response(200)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
            else:
                print("Ngrok URL not found. Make sure Ngrok is running and the NGROK_URL environment variable is set.")
        except Exception as e:
            self.send_error(500, f'Error sending response: {str(e)}')
