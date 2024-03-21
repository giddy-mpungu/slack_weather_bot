import http.server
import json

class SlackRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        # Parse request data
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        post_params = json.loads(post_data)

        # Extract city parameter from Slack's slash command
        city = post_params.get('text')

        # Validate city parameter
        if not city:
            self.send_error(400, 'Missing city parameter')
            return    

        # Process city parameter (to be implemented)

        # Send response
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        response_data = {'text': f"Received request for weather in {city}"}
        self.wfile.write(json.dumps(response_data).encode('utf-8'))

def run_server():
    server_address = ('', 8000)  # Change port if needed
    httpd = http.server.HTTPServer(server_address, SlackRequestHandler)
    print('Starting server...')
    httpd.serve_forever()

if __name__ == '__main__':
    run_server()
